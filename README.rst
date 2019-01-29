.. -*- coding: utf-8 -*-

================
PLONE JENKINS/CI
================
This repository is used to configure http://jenkins.plone.org

See ``docs/source/team.rst`` for the members of the Plone testing and CI team,
as well as their responsibilities.

Servers configuration
=====================
Our servers and nodes are configured with `ansible<http://ansible.com/>`_.

Jobs
====
A jenkins server without any job is quite useless.

All our jenkins jobs are configured through `jenkins-job-builder<https://pypi.python.org/pypi/jenkins-job-builder>`_.

See the `documentation<https://pypi.python.org/pypi/jenkins-job-builder>`_ on how to set them,
the actual configuration files are located at the ``jobs`` folder.
