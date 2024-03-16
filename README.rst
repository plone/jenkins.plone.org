.. -*- coding: utf-8 -*-

================
PLONE JENKINS/CI
================
This repository is used to configure http://jenkins.plone.org

Servers configuration
=====================
Our servers and nodes are configured with `ansible<http://ansible.com/>`_.

Jobs
====

Get the repository and python:

::
    git clone git@github.com:plone/jenkins.plone.org
    cd jenkins.plone.org
    python3.11 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

Test creating the jobs locally::

    jenkins-jobs --conf jobs/config.ini test jobs/jobs.yml -o output --config-xml
