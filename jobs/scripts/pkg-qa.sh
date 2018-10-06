#!/bin/sh
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.2/requirements.txt -O requirements.txt
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.2/experimental/qa.cfg -O qa.cfg
wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg

pip install -Ur requirements.txt
buildout buildout:git-clone-depth=1 code-analysis:directory={top-level} -c qa.cfg
bin/code-analysis
