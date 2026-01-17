#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_readme_roles.py

Universal README.md generator for Ansible roles in a project.
Supports multiple roles, auto-detects role name, description, author from meta/main.yml.
"""

import pathlib
import yaml
import re
import subprocess
import sys

ROOT = pathlib.Path('.')
README = ROOT / 'README.md'
BEGIN = '<!-- BEGIN AUTOGEN -->'
END = '<!-- END AUTOGEN -->'


def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        return f'[command failed]\n{e}\n'


def detect_role(role_arg=None):
    if role_arg:
        role_dir = ROOT / role_arg
        if (role_dir / 'tasks').exists() and (role_dir / 'meta' / 'main.yml').exists():
            return role_dir
        else:
            print(f'Role path {role_dir} invalid (missing tasks/ or meta/main.yml)')
            sys.exit(1)
    # auto-detect role in current folder
    candidates = [d for d in ROOT.iterdir() if d.is_dir() and (d / 'tasks').exists() and (d / 'meta' / 'main.yml').exists()]
    if not candidates:
        print('Не найдена структура роли (tasks/ и meta/main.yml) в текущей директории.')
        sys.exit(0)
    if len(candidates) > 1:
        print('Найдено несколько ролей, возьмем первую:', candidates)
    return candidates[0]


def read_meta(role_dir):
    meta_file = role_dir / 'meta' / 'main.yml'
    name = role_dir.name
    desc = ''
    author = ''
    if meta_file.exists():
        data = yaml.safe_load(meta_file.read_text())
        info = data.get('galaxy_info', {})
        desc = info.get('description', '')
        author = info.get('author', '')
    return name, desc, author


def tree_block(role_dir):
    return f"""## Project structure of role `{role_dir.name}`

```text
{run(f'tree {role_dir}')}```"""


def list_tasks_block(role_dir):
    playbook = ROOT / 'playbook.yml'
    return f"""## Ansible task list

```yaml
{run(f'ansible-playbook -i inventory.yml {playbook} --list-tasks')}```"""


def vars_block(role_dir):
    defaults_file = role_dir / 'defaults' / 'main.yml'
    if not defaults_file.exists():
        return ''
    data = yaml.safe_load(defaults_file.read_text()) or {}
    if not data:
        return ''
    rows = [f"| `{k}` | `{v}` |" for k, v in data.items()]
    return f"""## Default variables

| Variable | Default |
|---------|---------|
{chr(10).join(rows)}"""


def tasks_docs(role_dir):
    docs = ['## Role tasks\n']
    doc_start_re = re.compile(r'#\s*@doc:\s*(.+)')
    doc_cont_re = re.compile(r'#\s{2,}(.+)')
    name_re = re.compile(r'-\s+name:\s*(.+)')

    tasks_dir = role_dir / 'tasks'

    for task_file in sorted(tasks_dir.glob('*.yml')):
        docs.append(f'### {task_file.name}\n')
        current_doc = []
        task_names_after_doc = []
        for line in task_file.read_text().splitlines():
            m_start = doc_start_re.match(line)
            if m_start:
                current_doc = [m_start.group(1).strip()]
                continue
            m_cont = doc_cont_re.match(line)
            if m_cont and current_doc:
                current_doc.append(m_cont.group(1).strip())
                continue
            name_match = name_re.match(line)
            if name_match:
                task_name = name_match.group(1).strip('"')
                if current_doc:
                    docs.append(f'- **{current_doc[0]}**')
                    for subline in current_doc[1:]:
                        docs.append(f'  - {subline}')
                    current_doc = []
                    task_names_after_doc.append(task_name)
                else:
                    task_names_after_doc.append(task_name)
        for tname in task_names_after_doc:
            docs.append(f'- `{tname}`')
        docs.append('')
    return '\n'.join(docs)


def how_to_run():
    return '''## How to run

### Run playbook
```bash
ansible-playbook -i inventory.yml playbook.yml
```
### Run specific task by tag
```bash
ansible-playbook -i inventory.yml playbook.yml --tags TAG
```
### List all tasks
```bash
ansible-playbook -i inventory.yml playbook.yml --list-tasks
```
### Run with verbose output
```bash
ansible-playbook -i inventory.yml playbook.yml -Dv
```'''


def generate(role_arg=None):
    role_dir = detect_role(role_arg)
    role_name, role_desc, role_author = read_meta(role_dir)

    content_parts = [
        f'# {role_name}',
    ]
    if role_desc:
        content_parts.append(role_desc)
    if role_author:
        content_parts.append(f'**Author:** {role_author}')

    content_parts.extend([
        tree_block(role_dir),
        list_tasks_block(role_dir),
        tasks_docs(role_dir),
        vars_block(role_dir),
        how_to_run(),
    ])

    content = '\n\n'.join(content_parts)

    if README.exists():
        text = README.read_text()
        if BEGIN in text and END in text:
            text = re.sub(f'{BEGIN}.*?{END}', f'{BEGIN}\n{content}\n{END}', text, flags=re.S)
        else:
            text += f'\n{BEGIN}\n{content}\n{END}'
    else:
        text = f'{BEGIN}\n{content}\n{END}'

    README.write_text(text)


if __name__ == '__main__':
    role_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate(role_arg)
    print('README.md successfully updated')
