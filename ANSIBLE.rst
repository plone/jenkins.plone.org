Create and activate virtualenv:

  $ virtualenv .env
  $ source .env/bin/activate

Install Ansible:

  $ pip install ansible

Change inventory.txt and make sure that you can connect to the machines listed there.

Run Playbook:

  $ ansible-playbook jenkins_slave.yml -i inventory.txt
