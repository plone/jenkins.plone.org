# buildout and core tests (no AT nor robot)
$PYTHON27 bootstrap.py --setuptools-version=18.2 -c jenkins.cfg
bin/buildout -c jenkins.cfg
bin/alltests --xml
