#!/bin/bash
# buildout and core tests (no AT nor robot)
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
$PYTHON27 bootstrap.py --setuptools-version=19.4 -c jenkins.cfg
bin/buildout -c jenkins.cfg
bin/alltests --xml