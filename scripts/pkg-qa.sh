#!/bin/bash
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/bootstrap.py -O bootstrap.py
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/experimental/qa.cfg -O qa.cfg
wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg
sed -i 's#directory = src#directory = {top-level}#' qa.cfg
$PYTHON27 bootstrap.py --setuptools-version 21.0.0 -c qa.cfg
./marker.sh set $$
bin/buildout -c qa.cfg
./marker.sh release
bin/code-analysis
