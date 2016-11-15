.. -*- coding: utf-8 -*-

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
to test changes before sending a pull request is extremely helpful.

For this `vagrant <http://vagrantup.com/>`_ is a perfect fit.

Set up
======
- install vagrant and its dependencies and everything said on :doc:`setup`
- from within a clone of jenkins.plone.org repository checkout run:

.. code-block:: shell

    vagrant up master
    vagrant up node

``vagrant`` will automatically run the ansible playbook for them.

If the playbook fails, run:

.. code-block:: shell

    vagrant provision master
    vagrant provision node

And that will re-run the ansible playbook once again,
and hopefully fixing the previous problem.

You can enjoy your newly jenkins.plone.org master server locally at:

``http://localhost:8080``

.. note::
   There seems to be some problems with nginx.

   POST requests get the port (8080) removed on the response.
   Adding the port back on the wrong URL makes it work again.

Finally, to run ``jenkins-job-builder`` on it, run:

.. code-block:: shell

    jenkins-jobs --conf jenkins.ini.in update jobs.yml

*Enjoy!*
