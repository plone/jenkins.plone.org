#!/bin/bash
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/bootstrap.py -O bootstrap.py
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/experimental/qa.cfg -O qa.cfg
wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg
sed -i 's#directory = src#directory = {top-level}#' qa.cfg
$PYTHON27 bootstrap.py --setuptools-version 33.1.1 --buildout-version 2.8.0 -c qa.cfg
bin/buildout -c qa.cfg
bin/code-analysis
