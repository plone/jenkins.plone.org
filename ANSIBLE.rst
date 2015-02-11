===============================
How to Set Up jenkins.plone.org
===============================

There are two main steps:

- install jenkins master and nodes (done with ansible, see below)
- configure jenkins jobs (done with jenkins-job-builder, see futher below)


Install jenkins master and nodes
================================

Checkout this repository::

  $ git clone git@github.com:plone/jenkins.plone.org.git 
  $ cd jenkins.plone.org

Create and activate virtualenv::

  $ virtualenv .env
  $ source .env/bin/activate

Install Ansible::

  $ pip install ansible

Fetch Ansible Galaxy Dependencies as Git Submodules::

  $ git submodule init
  $ git submodule update

Change inventory.txt and make sure that you can connect to the machines listed there.

Copy your public ssh key to the machine::

  $ ssh-copy-id -i ~/.ssh/<SSH-KEY>.pub root@<SERVER_IP>

Run Playbook::

  $ ansible-playbook -i inventory.txt jenkins.plone.org.yml


Manual Configuration
--------------------

We will automate this later.

Manage Jenkins -> Configure System:

* # of executors: 0
* System Admin e-mail address: tisto@plone.org

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

PYTHON:/usr/bin/python2.7
PYTHON27:/usr/bin/python2.7
PYTHON26:/usr/bin/python2.6


Configure jenkins jobs
======================

*Do the steps described above to clone,
activate virtualenv and fetch submodules*.

Put jenkins-job-builder in development mode::

  $ cd src/jenkins-job-builder
  $ python setup.py develop

Put this repository also on development mode::

  $ cd ../..  # go back to the root
  $ python setup.py develop

.. note::
   Activate first jenkins-job-builder **and** later jenkins.plone.org so that
   you don't end up with two versions of jenkins-job-builder on the virtualenv.

Test the jobs are properly setup::

  $ jenkins-jobs test jobs.yml -o output

.. note::
   A folder named ``output`` should contain one file per each jenkins job
   configured on jobs.yml

Put your credentials on ``jenkins.ini`` (see the file for how to get them).

Now finally install the jobs on the server::

  $ jenkins-jobs --conf jenkins.ini update jobs.yml
