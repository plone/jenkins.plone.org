#!/bin/sh
# checkout all packages
pip install -Ur requirements.txt
buildout buildout:git-clone-depth=1 -c core.cfg

wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg

buildout \
  'buildout:bin-directory=../bin' \
  'buildout:parts-directory=../parts' \
  'code-analysis:jenkins=False' \
  -c experimental/qa.cfg

blacklist="Plone plone.themepreview diazo jquery.recurrenceinput.js mockup mockup-core"
for pkg in src/*;
do
    if [ "$(echo $blacklist | grep -c $pkg)" -eq 0 ]; then
        echo "$pkg"
        bin/code-analysis "$pkg"
    fi
done | tee qa.txt
