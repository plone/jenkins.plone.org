#!/usr/bin/env bash
ansible-playbook --limit jenkins_nodes -i inventory.txt jenkins_node.yml
