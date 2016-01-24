# buildout, core and AT tests
$PYTHON27 bootstrap.py --setuptools-version=19.4 -c {buildout}
bin/buildout -c {buildout}
bin/alltests --xml --all
bin/alltests-at --xml
