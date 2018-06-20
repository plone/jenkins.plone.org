#!/bin/bash
# checkout all packages
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c core.cfg

sed -i 's#jenkins = True#jenkins = False#' experimental/qa.cfg
sed -i 's#\[buildout\]#\[buildout\]\nbin-directory = ../bin#' experimental/qa.cfg
sed -i 's#\[buildout\]#\[buildout\]\nparts-directory = ../parts#' experimental/qa.cfg
wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg

buildout -c experimental/qa.cfg

echo "" > qa.txt
blacklist="Plone plone.themepreview diazo jquery.recurrenceinput.js mockup mockup-core"
for pkg in src/*;
do
    if [ `echo $blacklist | grep -c $pkg` -eq 0 ]; then
        echo $pkg
        bin/code-analysis $pkg >> qa.txt
    fi
done
