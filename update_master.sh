#!/usr/bin/env bash
ansible-playbook --limit jenkins_server -i inventory.txt jenkins_server.yml
