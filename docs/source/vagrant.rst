=========================
Testing locally (vagrant)
=========================

As collaborative configuration of servers is really useful to spread knowledge,
so it is also that one can step on each others toes,
or not be sure if a server can be really be used for testing,
or if others are *already* testing on it while you also want to test...

So to make it short and easy:
having a local environment
(i.e. virtual image)
to test changes before sending a pull request is extremly helpful.

For this `vagrant <http://vagrantup.com/>`_ is a perfect fit.


Set up
======

* install vagrant and its dependencies and everything said on :doc:`setup`
* from within a clone of jenkins.plone.org repository checkout run::

    vagrant up
    ssh-copy-id vagrant@127.0.0.1 -p 2222 # so that you can ssh without being asked for the password
    ansible-playbook -i inventory.txt jenkins_local.yml

*Enjoy!*
