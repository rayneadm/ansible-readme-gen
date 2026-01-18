# ansible-readme-gen

ansible-readme-gen is a simple tool to automatically generate README.md files for Ansible roles.
How it looks [Auto generated README](https://github.com/rayneadm/ansible-prepare-os/blob/main/README.md)

It scans the project directory, detects Ansible role structure, and generates documentation based on:
- role metadata (meta/main.yml)
- task files (../tasks/*.yml)
- default variables (../default/main.yml)
- project structure

The tool is packaged as a Docker image to avoid local Python dependency issues.

⸻

## Features
- Auto-detect Ansible roles
- Generate project structure (tree)
- List Ansible tasks
- Document default variables
- Update README.md automatically
- No local Python setup required

⸻

## Requirements
- Installed [Docker](https://docs.docker.com/engine/install/)
- Ansible role structure in the current directory

### For example:

`% pwd`
../ansible-prepare-os
`% tree`
```yaml
.
├── playbook.yml
├── prepare
│   ├── defaults
│   │   └── main.yml
│   ├── files
│   │   ├── custom
│   │   └── motd
│   ├── meta
│   │   └── main.yml
│   └── tasks
│       ├── main.yml
│       ├── packages.yml
│       ├── profile.yml
│       ├── root.yml
│       └── users.yml
└── README.md

6 directories, 12 files
```


⸻

## Usage

Pull the image:
```bash
docker pull rayneadm/ansible-readme-gen:latest
```
or from GitHub Container Registry:
```bash
docker pull ghcr.io/rayneadm/ansible-readme-gen:latest
```
- But also you can make you own local image

Run the generator in your project directory:
```bash
docker run --rm -v "$PWD:/data" -w /data rayneadm/ansible-readme-gen
```
The README.md file will be created or updated in the current directory.



```bash
git clone git@github.com:rayneadm/ansible-readme-gen.git
cd ansible-readme-gen
docker build -t rayneadm/ansible-readme-gen:latest .
docker run --rm -v "$PWD:/data" -w /data rayneadm/ansible-readme-gen
```


⸻

## Project structure
```yaml
.
├── app
│   └── generate_readme.py
├── Dockerfile
├── generate.sh
├── LICENSE
├── README.md
└── requirements.txt
```
