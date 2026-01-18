#!/bin/bash
docker pull rayneadm/ansible-readme-gen:latest
docker run --rm -v "$PWD:/data" -w /data rayneadm/ansible-readme-gen
