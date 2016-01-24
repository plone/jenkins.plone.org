# buildout and robot tests
$PYTHON27 bootstrap.py --setuptools-version=19.4 -c jenkins.cfg
bin/buildout -c jenkins.cfg
ROBOTSUITE_PREFIX=ONLYROBOT
bin/alltests -t ONLYROBOT --all --xml
