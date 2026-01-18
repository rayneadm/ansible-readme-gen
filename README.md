# ansible-readme-gen

**ansible-readme-gen** is a simple tool to automatically generate **README.md** files for Ansible roles.   

Tool scans the project directory, detects Ansible role structure, and generates documentation based on:
- role metadata (meta/main.yml)
- task files (../tasks/*.yml)
- default variables (../default/main.yml)
- project structure   

The tool is packaged as a Docker image to avoid local Python dependency issues.

## Features
- Auto-detect Ansible roles
- Generate project structure (tree)
- List Ansible tasks
- Document default variables
- Update README.md automatically
- No local Python setup required

### ansible-readme-gen README.md strucrure
> #### Ansible role name
> *role name and description from metadata*
> #### Project structure
> *list of* **tree** command
> #### Ansible task list
> *list of command **ansible-playbook playbook.yml --task--list**
> #### Role tasks 
> *and description lile below*
> > ##### main.yml
> > - **List all tasks of this role**
> > - - This is the better place for include your jobs
> > - Setting for root
> > - Setting for users
> > - Profile tings
> > - Install packages
> >
> > ##### packages.yml
> > - **Install packages for Debian and RHEL OS family**
> > - - To change list of packages edit: default/main.yml
> > - - To run this task use tag -t packages
> > - Update apt cache (Debian)
> > - Install common packages
> > - Install Debian packages
> > - Install RHEL packages
> #### **Default variables**
> *Varibles from ../default/main.yml*
> #### **How to run**
> *just reminder how to run this role*

Look example how it works: [Auto generated README](https://github.com/rayneadm/ansible-prepare-os/blob/main/README.md)

## Requirements
- Installed [Docker](https://docs.docker.com/engine/install/)
- Ansible role structure in the current directory
- Added descriptions in the task

### For example:
```yaml
# Run this tool in the root of ansible role
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
│       ├── main.yml  # Add description in this files
│       ├── packages.yml # and there
│       ├── profile.yml # ...
│       ├── root.yml # ...
│       └── users.yml # ...
└── README.md # Will be generet in the root of ansible role

6 directories, 12 files
```

### About description format
This one an example, how to discribe you playbooks:   
```yaml
# @doc: Install custom motd
#  - Also install some varables
#  - *To run this task use tag* `-t profile`

---
- name: Deploy global shell environment
  ansible.builtin.copy:
...
..
.
```

Just add descritpion in the head of task.    
First line have to contain flag **@doc**, for the next lines you can use **Markdown** format.  
Look [examples](https://github.com/rayneadm/ansible-prepare-os/blob/main/prepare/tasks/profile.yml) of description.    

## Usage

Pull the image:
```bash
docker pull rayneadm/ansible-readme-gen:latest
```
or from GitHub Container Registry:
```bash
docker pull ghcr.io/rayneadm/ansible-readme-gen:latest
```

Run the generator in your project directory:
```bash
docker run --rm -v "$PWD:/data" -w /data rayneadm/ansible-readme-gen
```
The README.md file will be created or updated in the current directory.


### But also you can make you own local image

```bash
git clone git@github.com:rayneadm/ansible-readme-gen.git
cd ansible-readme-gen
docker build -t rayneadm/ansible-readme-gen:latest .
docker run --rm -v "$PWD:/data" -w /data rayneadm/ansible-readme-gen
```

## Ansible inventory ..
If you dont have inventory file in your project when you run this tool, you'll see *Ansible warning*.
```bash
[WARNING]: Unable to parse /data/inventory.yml as an inventory source
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available.
```
This is not mistake it's just worning, dont wory.
