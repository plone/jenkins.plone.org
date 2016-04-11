.. -*- coding: utf-8 -*-

=====================
Run pull request jobs
=====================
Before merging a pull request on GitHub (or manually via the command line),
one needs to be sure that nothing breaks due to the changes made on the pull request.

For that we have some special jenkins job meant for that:

- If the pull request targets Plone 5.1: http://jenkins.plone.org/job/pull-request-5.1
- If the pull request targets Plone 5.0: http://jenkins.plone.org/job/pull-request-5.0
- If the pull request targets Plone 4.3: http://jenkins.plone.org/job/pull-request-4.3

If the pull request targets **both** 5.1 *and* 5.0 you need to run a job on each of the jenkins jobs mentioned above.

Test a pull request
===================
To test a pull request with this jenkins job one only needs to do the following:

- go to http://jenkins.plone.org
- log in with your github user
- click on the `Pull Request 5.1 job <http://jenkins.plone.org/job/pull-request-5.1>`_
  or `Pull Request 4.3 job <http://jenkins.plone.org/job/pull-request-4.3>`_ if you are targeting that Plone version
- click on the huge button **Build with Parameters**
  `Plone 5.1 <http://jenkins.plone.org/job/pull-request-5.0/build?delay=0sec>`_ or
  `Plone 4.3 <http://jenkins.plone.org/job/pull-request-4.3/build?delay=0sec>`_
- paste the pull request URL on the text field
  (or multiple pull requests if they have to be combined, then one per line),
  like for example https://github.com/plone/plone.outputfilters/pull/16
- click on the ``Build`` button

If a video suits you best: https://youtu.be/mXs_OcJhjnU

GitHub integration
==================
As soon as the job starts the pull request on GitHub will be notified,
showing that the pull request is being tested by jenkins.plone.org.

When it finishes,
GitHub will be notified again and either report that all tests passed,
or that there has been some failures and thus it would not be wise to merge the pull request.

Mail integration
================
Reporting is not only done via GitHub, but also by email.

When the jenkins job is finished it will report by mail to the user that started the jenkins job.

On the mail,
the status of the job and a link to the jenkins job itself and to the pull request(s) are provided for convenience.

