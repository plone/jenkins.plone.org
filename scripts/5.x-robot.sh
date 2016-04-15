#!/bin/bash
# buildout and robot tests
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
$PYTHON27 bootstrap.py --setuptools-version 21.0.0 -c jenkins.cfg
./marker.sh set $$
bin/buildout -c jenkins.cfg
./marker.sh release
ROBOTSUITE_PREFIX=ONLYROBOT
bin/alltests -t ONLYROBOT --all --xml
