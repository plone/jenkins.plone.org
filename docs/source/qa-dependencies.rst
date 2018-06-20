.. -*- coding: utf-8 -*-

==========================
Check package dependencies
==========================
Systems evolve over time, new ideas come in and old ones go away.

As simple and logic as it reads,
the problem with the sentence above is the *going away* part.

To remove/deprecate a complete package (say ``Products.ATContentTypes``),
one first needs to know where it is being used,
then, one by one, keep updating all packages to remove that dependency.

Only after *all packages* have removed all traces of that package,
it can be safely removed.

But wait, during that time,
could it be that someone reintroduced a reference to that package?

Or to begin with,
how do we know which packages are the ones that need to be ported?

*I'm glad you ask.*

By carefully keeping the list of packages needed by a package,
and a way to keep track if new dependencies are added or removed,
one can then really be sure that a package is free from another one.

Tracking dependencies
=====================
In Python there is usually always a tool available, also for dependencies tracking:
enter `z3c.dependencychecker <https://pypi.org/project/z3c.dependencychecker>`_.

``z3c.dependencychecker`` is a tool that scans a package structure
(after its ``egg_info`` directory is built,
either by buildout or directly calling ``setup.py``)
and generates various reports regarding dependencies.

It not only tells you which dependencies are missing in ``setup.py``,
but also which dependencies are not needed,
which dependencies are missing for tests,
and which ones should be only test dependencies rather than general dependencies.

As life is complex,
there are quite a few packages that can not be correctly identified,
or packages that are soft dependencies, and thus they should not be made mandatory.

For these cases,
``z3c.dependencychecker`` also has an answer: ``.pyproject.toml``.

In this configuration file, expected to be found on the repository top level,
a table (in TOML parlance) is expected to help ``z3c.dependencychecker`` know about these corner cases.

For example, given this content:

::
    [tool.dependencychecker]
    ignore-packages = ['plone.app.dexterity' ]
    Zope2 = ['Products.Five', 'Products.OFSP']
    ZODB = ['ZEO', 'Pizza']

Any reference to ``plone.app.dexterity`` will not be reported,
while any references to ``Products.Five`` and ``Products.OFSP`` will be treated as if they were ``Zope2`` references,
and the same goes for ``ZODB``, ``ZEO`` and ``Pizza``.

With all these, one can get ready to clean a package dependencies.

See `z3c.dependency on pypi <https://pypi.org/project/z3c.dependencychecker>`_ for more details.

Clean a package
===============
On `Plone Jenkins <https://jenkins.plone.org>`_
there is a `Jenkins Job <https://jenkins.plone.org/job/qa-pkg-dependencies>`_ that reports if a package has its dependencies correctly defined.

You can use it to check what's the status of a package,
or to verify that the changes you made on it are indeed correct.

To use it, follow this instructions:

Log in with your GitHub account in Jenkins and click on the ``Build with Parameters`` button on the job page.

A form with two fields will show up:
type the package name (i.e. ``plone.app.dexterity``)
and the branch to test (i.e. ``master``) and click on the ``Build`` button.

A Jenkins job will be started.

As soon as it finishes,
it will report by email the ``z3c.dependencychecker`` report to you.

Take that report and fix the package's ``setup.py``,
add the ``.pyproject.toml`` on it with the ``[tool.dependencychecker]``
(even if it is no needed)
and make a pull request with everything.

As soon as there is this ``.pyproject.toml`` with the ``[tool.dependencychecker]``,
Jenkins (via `mr.roboto <https://github.com/plone/mr.roboto>`_)
will start automatically that job and report back on the pull request itself.

Work locally
------------
To check the random status of a package,
or simply if a package needs clean up,
the jenkins job is indeed useful.

But to actually work on cleaning a package it can be a bit cumbersome,
as you have to keep switching from your editor+terminal, the browser to check Jenkins output and your email client to get the reports.

For that a new ``part`` in ``buildout.coredev`` GitHub project was added: ``dependencies``.

To clean a package do the following:

- get ``buildout.coredev`` repository
- switch to branch 5.2
- remove all checkouts and leave/add only the package that you want to clean up on ``checkouts.cfg``
- virtualenv + bootstrap + buildout
- run dependencychecker on the package
- repeat the last two steps (see below) until the output is completely clean up

```
git clone https://github.com/plone/buildout.coredev
cd buildout.coredev
git checkout 5.2
${EDITOR} checkouts.cfg
virtualenv .
pip install -r requirements.txt
buildout -c core.cfg install dependencies
./bin/dependencychecker src/${PACKAGE}
```

.. note:: The idea of changing ``checkouts.cfg`` is to speed up the buildout run.

   For that, the ``install`` command on buildout allows also to only install a single part,
   thus, further speeding up the process.


**Congratulations, you helped cleaning up a package!!**
