.. -*- coding: utf-8 -*-

=======
Servers
=======
http://jenkins.plone.org runs on a number of different servers, see below.

Master
======
- hosted at hetzner.de
- IP: 78.47.49.108
- donor: Timo Stollenwerk
- contact: Timo Stollenwerk (tisto) and Gil Forcada (gforcada)

Nodes
=====

Current nodes
-------------
- hosted at Rackspace
- IPs: 23.253.244.222 104.130.135.173 23.253.61.36
- donor: Rackspace
- contact: Sven (svx) and Gil Forcada (gforcada)

New nodes server
----------------
- hosted at hetzner.de
- IP: 88.99.26.113 / 2a01:4f8:10a:2ae::2
- donor: Plone Foundation
- contact: Paul Roeland (polyester) and Gil Forcada (gforcada)

Configuration
*************
Base system: Ubuntu 16.04 LTS minimal

Install lxd:

.. code-block:: shell

    apt-get install lxd

Initial configuration:

.. code-block:: shell

    lxd init
    (all default options)

Create nodes:

.. code-block:: shell

    lxc launch ubuntu:16.04 node1
    lxc launch ubuntu:16.04 node2
    lxc launch ubuntu:16.04 node3

Add SSH keys:

.. code-block:: shell

    lxc file push /root/.ssh/authorized_keys node1/root/.ssh/authorized_keys
    lxc file push /root/.ssh/authorized_keys node2/root/.ssh/authorized_keys
    lxc file push /root/.ssh/authorized_keys node3/root/.ssh/authorized_keys

Write down nodes IPs:

.. code-block:: shell

    lxc list

Configure a jump host to connect to them:

.. code-block:: config

    Host jenkins-plone-org-nodes-host
      HostName 88.99.26.113
      User root
      ProxyCommand none

    Host node1-jenkins-plone-org
      HostName XX.XX.XX.XX
      User root
      ProxyCommand ssh jenkins-plone-org-nodes-host nc %h %p 2> /dev/null

    Host node2-jenkins-plone-org
      HostName XX.XX.XX.XX
      User root
      ProxyCommand ssh jenkins-plone-org-nodes-host nc %h %p 2> /dev/null

    Host node3-jenkins-plone-org
      HostName XX.XX.XX.XX
      User root
      ProxyCommand ssh jenkins-plone-org-nodes-host nc %h %p 2> /dev/null

Connect to all nodes to accept their fingerprint:

.. code-block:: shell

    ssh node1-jenkins-plone-org
    ssh node2-jenkins-plone-org
    ssh node3-jenkins-plone-org

Install python 2.7 (as ansible still needs it):

.. code-block:: shell

    ssh node1-jenkins-plone-org "apt-get update && apt-get install -y python2.7"
    ssh node2-jenkins-plone-org "apt-get update && apt-get install -y python2.7"
    ssh node3-jenkins-plone-org "apt-get update && apt-get install -y python2.7"

Add iptables rules to let jenkins master connect to the nodes,
these two lines are needed **for each** node:

.. code-block:: shell

    iptables -t nat -A PREROUTING -p tcp --dport ${SPECIFIC_PORT} -j DNAT --to-destination ${NODE_IP}:22
    iptables -t nat -A POSTROUTING -p tcp -d ${NODE_IP} --dport ${SPECIFIC_PORT} -j SNAT --to-source ${SERVER_IP}

.. note:: update SPECIFIC_PORT to something like 808X (each node a different port),
   NODE_IP to the IP of each node (node IP can be seen with ``lxc list``)
   and SERVER_IP to the server host (i.e. 88.99.26.113)

TODO
^^^^
- create ansible playbook for bootstrap the server so it does:

  - create containers with ansible
  - configure SSH
  - install python2.7 on containers
  - configure firewall
