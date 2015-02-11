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

