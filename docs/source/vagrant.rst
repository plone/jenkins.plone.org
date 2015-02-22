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

Yes,
that's it,
``vagrant`` will automatically run the ansible playbook.

If,
for whichever reason,
the playbook fails,
just run::

  vagrant provision

And that will re-run the ansible playbook once again,
and hopefully fixing the previous problem.

*Enjoy!*
