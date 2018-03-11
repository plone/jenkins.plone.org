#!/usr/bin/env bash
# checkout all packages
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' jenkins-package-dependencies.cfg
pip install -r requirements.txt
buildout -c jenkins-package-dependencies.cfg install dependencies

echo "" > deps.txt

blacklist="Plone plone.themepreview ZODB3 diazo jquery.recurrenceinput.js mockup txtfilter"
cd src
for pkg in *;
do
    if [ `echo $blacklist | grep -c $pkg` -eq 0 ];
    then
        cd $pkg
        echo $pkg >> ../../deps.txt
        ../../bin/dependencychecker >> ../../deps.txt
        cd ..
    fi
done
