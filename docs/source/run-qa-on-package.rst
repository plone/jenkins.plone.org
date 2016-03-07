.. -*- coding: utf-8 -*-

==============================
Run code analysis on a package
==============================

Our `jenkins.plone.org`_ is running code analysis (via `plone.recipe.codeanalysis`_) on a number of packages,
`see the up-to-date list`_.

Follow these steps to check how any arbitrary package adheres to our Plone official guidelines.

.. note::
   See the `very same script`_ that Jenkins uses,
   below follows a more detailed step to step on how to run it and fix the errors.

Clone the repository and create a Python virtual environment::

    git clone git@github.com:plone/plone.app.discussion.git
    cd plone.app.discussion
    virtualenv .
    source bin/activate

Create a cleanup branch,
although not mandatory it's always a good idea::

    git checkout -b cleanup

Get the QA configuration and bootstrap::

    wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/bootstrap.py -O bootstrap.py
    wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/experimental/qa.cfg -O qa.cfg
    wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg

    python bootstrap.py --setuptools-version 19.4 -c qa.cfg

Adjust ``qa.cfg`` to the package:

- check that the ``directory`` option on ``code-analysis`` part matches the top-level folder of the distribution
- remove the ``jenkins = True`` line (so that ``bin/code-analysis`` shows its report on the terminal)

Finally run buildout and code analysis::

    bin/buildout -c qa.cfg
    bin/code-analysis

The first easy fixes can be easily solved with ``autopep8`` and ``isort``::

    pip install autopep8 isort

    isort plone/app/discussion/*.py
    autopep8 --in-place -r plone/app/discussion

By default autopep8 does white space only changes which are basically guaranteed safe.

**Important** exception: undo any changes made by autopep8 to Python **skin** scripts.
For instance, it will change the double comment hashes at the top to single hashes,
which completely break those Python scripts.

After committing the initial autopep8 run,
you can run autopep8 in more aggressive mode,
but you have to check these changes more carefully::

   autopep8 --in-place --ignore W690,E711,E721 --aggressive

Keep running ``bin/code-analysis`` to see how much errors are still left to be fixed.

Once finished,
add a comment on ``CHANGES.rst`` and commit all the changes in a single commit::

    $EDITOR CHANGES.rst

    git commit -am"Cleanup"

Push the branch::

    git push -u

Create a pull request on github and start a jenkins job to verify that your changes did not break anything.
For that, paste the pull request URL on this form (once authenticated via github)::

    http://jenkins.plone.org/job/pull-request-5.1/build?delay=0sec

Lastly `file an issue on jenkins.plone.org issue tracker`_ so that Jenkins start monitoring the package.

**Done! Thanks for cleaning one package!**

  .. _jenkins.plone.org: http://jenkins.plone.org
  .. _plone.recipe.codeanalysis: https://pypi.python.org/pypi/plone.recipe.codeanalysis
  .. _very same script:  https://raw.githubusercontent.com/plone/jenkins.plone.org/master/scripts/pkg-qa.sh
  .. _file an issue on jenkins.plone.org issue tracker: https://github.com/plone/jenkins.plone.org/issues/new
  .. _see the up-to-date list: http://jenkins.plone.org/view/Pkgs
