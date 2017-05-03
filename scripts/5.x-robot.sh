#!/bin/bash
# buildout and robot tests
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
$PYTHON27 bootstrap.py --setuptools-version 33.1.1 --buildout-version 2.8.0 -c jenkins.cfg
bin/buildout -c jenkins.cfg
ROBOTSUITE_PREFIX=ONLYROBOT
bin/alltests -t ONLYROBOT --all --xml
