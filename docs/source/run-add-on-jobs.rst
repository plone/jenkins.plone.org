.. -*- coding: utf-8 -*-

===============
Run add-on jobs
===============
Before a final release of Plone core is done,
add-ons might want to check if they need any porting effort to make the add-on compatible with it.

For that we have some special jenkins jobs:

- If the add-on targets Plone 5.1: http://jenkins.plone.org/job/test-addon-5.1
- If the add-on targets Plone 5.0: http://jenkins.plone.org/job/test-addon-5.0
- If the add-on targets Plone 4.3: http://jenkins.plone.org/job/test-addon-4.3

Test an add-on
==============
- go to http://jenkins.plone.org
- log in with your github user
- click on the `Test add-on against Plone 5.2 job <http://jenkins.plone.org/job/test-addon-5.2>`_
  or `Test add-on against Plone 5.1 job <http://jenkins.plone.org/job/test-addon-5.1>`_
  or `Test add-on against Plone 5.0 job <http://jenkins.plone.org/job/test-addon-5.0>`_
  or `Test add-on against Plone 4.3 job <http://jenkins.plone.org/job/test-addon-4.3>`_ if you are targeting that Plone version
- click on the huge button **Build with Parameters**
  `Plone 5.2 <http://jenkins.plone.org/job/test-addon-5.2/build?delay=0sec>`_ or
  `Plone 5.1 <http://jenkins.plone.org/job/test-addon-5.1/build?delay=0sec>`_ or
  `Plone 5.0 <http://jenkins.plone.org/job/test-addon-5.0/build?delay=0sec>`_ or
  `Plone 4.3 <http://jenkins.plone.org/job/test-addon-4.3/build?delay=0sec>`_
- paste the add-on git URL for the add-on that you want to test on the ``ADDON_URL`` field,
  for example https://github.com/collective/collective.cover.git
- *(optionally)* type the branch you want to test the add-on against on the ``ADDON_BRANCH`` field,
  by default it will be the master branch
- click on the ``Build`` button

.. note::
   For the jobs to work properly they need to get the add-on name out of the URL,
   for that, the last path of the URL will be used,
   i.e. https://github.com/my-org/my-cool-repo.git or https://gitlab.com/another-org/project/something/else/my-cool-repo.git
   If not the add-on name can not be guessed with a regular expression.

GitHub integration
==================
A comment will be added on the latest commit on that branch once the job finishes.

Mail integration
================
When the jenkins job is finished it will report by mail to the user that started the jenkins job.

On the mail,
the status of the job will be provided.
