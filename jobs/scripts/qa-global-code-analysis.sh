#!/bin/sh
set -x

# checkout all packages
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c core.cfg

wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg

buildout \
  code-analysis:jenkins=False \
  buildout:bin-directory=../bin \
  buildout:parts-directory=../parts \
  -c experimental/qa.cfg

ignorelist="Plone plone.themepreview diazo jquery.recurrenceinput.js mockup mockup-core"
for pkg in src/*;
do
    if [ "$(echo $ignorelist | grep -c $pkg)" -eq 0 ]; then
        echo "$pkg"
        bin/code-analysis "$pkg"
    fi
done | tee qa.txt
