#!/usr/bin/env bash
ansible-playbook --limit jenkins_nodes -i ansible/inventory.txt ansible/node.yml
