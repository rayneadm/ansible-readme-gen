# ansible-readme-gen

ansible-readme-gen is a simple tool to automatically generate README.md files for Ansible roles.

It scans the project directory, detects Ansible role structure, and generates documentation based on:
	•	role metadata (meta/main.yml)
	•	task files
	•	default variables
	•	project structure

The tool is packaged as a Docker image to avoid local Python dependency issues.

⸻

## Features
	•	Auto-detect Ansible roles
	•	Generate project structure (tree)
	•	List Ansible tasks
	•	Document default variables
	•	Update README.md automatically
	•	No local Python setup required

⸻

## Requirements
	•	Docker
	•	Ansible role structure in the current directory

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
Run the generator in your project directory:
```bash
docker run --rm -v "$PWD:/data" -w /data rayneadm/ansible-readme-gen
```
The README.md file will be created or updated in the current directory.

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
