==============================
jenkins.plone.org Set Up Howto
==============================

This document describes how to set up the entire Jenkins infrastructure for jenkins.plone.org.
Those are the main steps:

  * Set up Jenkins server (jenkins.plone.org, with Ansible)
  * Set up Jenkins node (node[1-x].jenkins.plone.org, with Ansible)
  * Set up the Jenkins jobs on the Jenkins server (with Jenkins Job Builder)


Prerequisites
=============

Checkout this repository::

  $ git clone git@github.com:plone/jenkins.plone.org.git
  $ cd jenkins.plone.org

Create and activate virtualenv::

  $ virtualenv .env
  $ source .env/bin/activate

Install Ansible::

  $ pip install ansible

Fetch Ansible Galaxy Dependencies as Git Submodules::

  $ git submodule update --init

Change inventory.txt and make sure that you can connect to the machines listed there.

Copy your public ssh key to the machine::

  $ ssh-copy-id -i ~/.ssh/<SSH-KEY>.pub root@<SERVER_IP>


Set Up Jenkins Server
---------------------

::

  $ ansible-playbook -i inventory.txt jenkins_server.yml


Set Up Jenkins Nodes
--------------------

::

  $ ansible-playbook -i inventory.txt jenkins_nodes.yml


Set Up Jenkins Jobs
-------------------

*Do the steps described above to clone,
activate virtualenv and fetch submodules*.

Put jenkins-job-builder in development mode::

  $ cd src/jenkins-job-builder
  $ python setup.py develop

Test the jobs are properly setup::

  $ jenkins-jobs --conf jenkins.ini.in test jobs.yml -o output

.. note::
   A folder named ``output`` should contain one file per each jenkins job
   configured on jobs.yml

Create your own ``jenkins.ini`` by copying it from ``jenkins.ini.in``::

  $ cp jenkins.ini.in jenkins.ini

Add your own credentials to jenkins.ini.
You can find them when you log into Jenkins and copy your API token
(e.g. http://jenkins.plone.org/user/tisto/configure).

Now finally install the jobs on the server::

  $ jenkins-jobs --conf jenkins.ini update jobs.yml



Manual Jenkins Configuration
----------------------------

There are currently a few steps that we need to carry out manually.
We will automate them later.

Github post-commit hook for buildout.coredev:

* Go to https://github.com/plone/buildout.coredev/settings/hooks and add a 'http://jenkins.plone.org/github-webhook/' post-commit hook.

Manage Jenkins -> Configure System:

* # of executors: 0
* System Admin e-mail address: tisto@plone.org
* E-mail Notification:
  * SMTP Server: smtp.gmail.com
  * Use SSL: True
  * SMTP Port: 465
  * Reply-To Address: jenkins@plone.org
  * Use SMTP Authentication: True
    * User Name: jenkins@plone.org
    * Password: ...
 * Theme:
   * URL of theme CSS: https://rawgit.com/plone/jenkins.plone.org/master/jenkins.plone.org.css

Manage Jenkins -> Manage Credentials -> Add Credentials: SSH Username with private key:

* Scope: System
* Username: jenkins
* Description: jenkins.plone.org private ssh key
* Private Key: From a file on Jenkins master: File: /var/lib/jenkins/jenkins.plone.org

=> Upload jenkins.plone.org private ssh key manually to /var/lib/jenkins
=> chown jenkins:jenkins jenkins.plone.org

Manage Jenkins -> Manage Nodes -> New Node (Dumb node):

* # of executors: 1 (later 3)
* Remote root directory: /home/jenkins
* Labels: rackspace Ubuntu14.04 Python27
* Host: node1.jenkins.plone.org
* Credentials: jenkins (jenkins.plone.org private ssh key)
* Node Properties -> Environment variables:

::

  PYTHON:/usr/bin/python2.7
  PYTHON27:/usr/bin/python2.7
  PYTHON26:/usr/bin/python2.6
