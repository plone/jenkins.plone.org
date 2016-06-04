#!/bin/bash
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/bootstrap.py -O bootstrap.py
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/experimental/py3x-test.cfg -O test.cfg
sed -i 's#REPLACE_ME#{package}#' test.cfg
$PYTHON35 bootstrap.py --setuptools-version 21.0.0 -c test.cfg
bin/buildout -c test.cfg
bin/test
