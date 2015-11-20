# buildout, core and AT tests
$PYTHON27 bootstrap.py --setuptools-version=18.2 -c {buildout}
bin/buildout -c {buildout}
bin/alltests --xml --all
bin/alltests-at --xml
