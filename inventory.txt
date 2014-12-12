node1.jenkins.plone.org
node2.jenkins.plone.org
node3.jenkins.plone.org
node4.jenkins.plone.org


- hosts: test.jenkins.plone.org
  remote_user: root
  roles:
    - plone.jenkins_server

