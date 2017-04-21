.. -*- coding: utf-8 -*-

==============================
jenkins.plone.org Set Up Howto
==============================
This document describes how to set up the entire Jenkins infrastructure for jenkins.plone.org.
Those are the main steps:

- Set up Jenkins server (jenkins.plone.org, with Ansible)
- Set up Jenkins nodes (node[1-x].jenkins.plone.org, with Ansible)
- Set up the Jenkins jobs on the Jenkins server (with Jenkins Job Builder)

Prerequisites
=============
Checkout this repository:

.. code-block:: shell

    $ git clone git@github.com:plone/jenkins.plone.org.git
    $ cd jenkins.plone.org

Create and activate a virtualenv:

.. code-block:: shell

    $ virtualenv -p python2.7 .
    $ source ./bin/activate

Install all the tools needed (ansible, ansible roles and jenkins-job-builder):

.. code-block:: shell

    $ pip install -r requirements.txt
    $ ansible-galaxy install -r roles.yml
    $ git submodule update --init

Check inventory.txt and make sure that you can connect to the machines listed there.

Copy your public ssh key to all servers:

.. code-block:: shell

    $ ssh-copy-id -i ~/.ssh/<SSH-KEY>.pub root@<SERVER_IP>

Set Up Jenkins Server
---------------------
.. code-block:: shell

    $ ./update_master.sh

Set Up Jenkins Nodes
--------------------
.. code-block:: shell

    $ ./update_nodes.sh

Set Up Jenkins Jobs
-------------------
*Do the steps described above to clone,
activate virtualenv and fetch submodules*.

Put jenkins-job-builder in development mode:

.. code-block:: shell

    $ cd src/jenkins-job-builder
    $ pip install -r requirements.txt
    $ python setup.py develop

Test the jobs are properly setup:

.. code-block:: shell

    $ jenkins-jobs --conf jenkins.ini.in test jobs.yml -o output

.. note::
   A folder named ``output`` should contain one file per each jenkins job
   configured on jobs.yml

Create your own ``jenkins.ini`` by copying it from ``jenkins.ini.in``:

.. code-block:: shell

    $ cp jenkins.ini.in jenkins.ini

Add your own credentials to jenkins.ini.
You can find them when you log into Jenkins and copy your API token
(e.g. http://jenkins.plone.org/user/tisto/configure).

Create your own ``secrets.yml`` by copying it from ``secrets.yml.in``:

.. code-block:: shell

    $ cp secrets.yml.in secrets.yml

Add github API secrets that are needed for the github login functionality on jenkins.plone.org.
You can find those settings on plone organization in github:
https://github.com/organizations/plone/settings/applications

Look for the ``Plone Jenkins CI`` application name.

For the ``github_api_key`` you need a personal token
(from https://github.com/jenkins-plone-org github user).

Now finally install the jobs on the server:

.. code-block:: shell

    $ ./update_jobs.sh

Manual Configuration
--------------------
There are currently a few steps that we need to carry out manually.
We will automate them later.

1) Github post-commit hook for buildout.coredev:

* go to https://github.com/plone/buildout.coredev/settings/hooks
* create a new webhook with the following details:

  * Payload URL: http://jenkins.plone.org/github-webhook/
  * Content type: application/x-www-form-urlencoded
  * Secret: *nothing*
  * Which events would you like to trigger this webhook?: Send me everything
  * Active: yes

2) Manage Jenkins -> Configure System:

* E-mail Notification:

  * SMTP Server: smtp.gmail.com
  * Use SSL: True
  * SMTP Port: 465
  * Reply-To Address: jenkins@plone.org
  * Use SMTP Authentication: True

    * User Name: jenkins@plone.org
    * Password: ...

3) Manage Jenkins -> Manage Credentials -> Add Credentials: SSH Username with private key:

* Scope: System
* Username: jenkins
* Description: jenkins.plone.org private ssh key
* Private Key: From a file on Jenkins master: File: /var/lib/jenkins/jenkins.plone.org

=> Upload jenkins.plone.org private ssh key manually to /var/lib/jenkins
=> chown jenkins:jenkins jenkins.plone.org
