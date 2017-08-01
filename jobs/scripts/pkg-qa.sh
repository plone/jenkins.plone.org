#!/bin/bash
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/requirements.txt -O requirements.txt
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/experimental/qa.cfg -O qa.cfg
wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg
sed -i 's#directory = src#directory = {top-level}#' qa.cfg
pip install -r requirements.txt
buildout -c qa.cfg
bin/code-analysis
