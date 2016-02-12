#!/bin/bash
# buildout, core and AT tests
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
$PYTHON27 bootstrap.py --setuptools-version=19.4 -c {buildout}
bin/buildout -c {buildout}
bin/alltests --xml --all
bin/alltests-at --xml
