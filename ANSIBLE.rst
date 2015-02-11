===============================================================================
How to Set Up jenkins.plone.org
===============================================================================

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

  $ ansible-playbook -i inventory.txt test.jenkins.plone.org.yml


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

