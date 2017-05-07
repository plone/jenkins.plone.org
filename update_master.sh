#!/usr/bin/env bash
ansible-playbook --limit jenkins_server -i ansible/inventory.txt ansible/server.yml
