# buildout and AT tests
$PYTHON27 bootstrap.py --setuptools-version=19.4 -c jenkins.cfg
bin/buildout -c jenkins.cfg
bin/alltests-at --xml
