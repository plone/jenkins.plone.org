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

Nodes server 1
--------------
- hosted at hetzner.de
- IP: 88.99.26.113 / 2a01:4f8:10a:2ae::2
- donor: Plone Foundation
- contact: Paul Roeland (polyester) and Gil Forcada (gforcada)

Node 4
------
- hosted at hetzner.de
- IP: 46.4.157.69
- donor: Jens Klein
- contact: Jens Klein (jensens) and Gil Forcada (gforcada)

Nodes server 2
--------------
- hosted at hetzner.de
- IP: 136.243.46.143 / 2a01:4f8:212:e8c::2
- donor: Plone Foundation
- contact: Paul Roeland (polyester) and Gil Forcada (gforcada)

Nodes server 3
--------------
- hosted at hetzner.de
- IP: 136.243.44.103 / 2a01:4f8:212:c5a::2
- donor: Plone Foundation
- contact: Paul Roeland (polyester) and Gil Forcada (gforcada)

Configuration
*************
Base system: Ubuntu 18.04 LTS minimal

Install lxd:

.. code-block:: shell

    apt-get install lxd

Initial configuration:

.. code-block:: shell

    lxd init
    (all default options)

Be sure that enough space is given!
By default LXD from Ubuntu 18.04 creates a loop device with only ~30Gb of space,
if that's the case, do the following:

.. code-block:: shell

    truncate -s100G /var/lib/lxd/disks/more-space.img
    ld=$(losetup --show --find /var/lib/lxd/disks/more-space.img); echo "$ld"
    lxc storage create more-space btrfs source="$ld"

Create nodes:

.. code-block:: shell

    lxc launch ubuntu:18.04 node1 -s more-space
    lxc launch ubuntu:18.04 node2 -s more-space
    lxc launch ubuntu:18.04 node3 -s more-space

.. note::
   The ``-s`` parameter with its value are not needed,
   if the default storage is big enough already.

Add SSH keys:

.. code-block:: shell

    lxc file push /root/.ssh/authorized_keys node1/root/.ssh/authorized_keys
    lxc file push /root/.ssh/authorized_keys node2/root/.ssh/authorized_keys
    lxc file push /root/.ssh/authorized_keys node3/root/.ssh/authorized_keys

Write down nodes IPs:

.. code-block:: shell

    lxc list

Configure a jump host to connect to them:

.. code-block:: text

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
  - configure firewall
