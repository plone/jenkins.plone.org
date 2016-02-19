#!/bin/bash
# checkout all packages
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' jenkins-package-dependencies.cfg
$PYTHON27 bootstrap.py -c jenkins-package-dependencies.cfg
bin/buildout -c jenkins-package-dependencies.cfg

echo "" > qa.txt

sed -i 's#jenkins = True#jenkins = False#' experimental/qa.cfg
wget https://raw.githubusercontent.com/plone/plone.recipe.codeanalysis/master/.isort.cfg -O .isort.cfg

blacklist="Plone plone.themepreview diazo jquery.recurrenceinput.js mockup mockup-core"
cd src
for pkg in *;
do
    if [ `echo $blacklist | grep -c $pkg` -eq 0 ]; then

        cd $pkg
        cp ../../bootstrap.py bootstrap.py
        cp ../../experimental/qa.cfg qa.cfg
        cp ../../.isort.cfg .isort.cfg

        if [[ -d "src" ]]; then
            sed -i 's#directory = src#directory = src#' qa.cfg

        elif [[ -d "plone" ]]; then
            sed -i 's#directory = src#directory = plone#' qa.cfg

        elif [[ -d "collective" ]]; then
            sed -i 's#directory = src#directory = collective#' qa.cfg

        elif [[ -d "Products" ]]; then
            sed -i 's#directory = src#directory = Products#' qa.cfg

        elif [[ -d "five" ]]; then
            sed -i 's#directory = src#directory = five#' qa.cfg

        elif [[ -d "archetypes" ]]; then
            sed -i 's#directory = src#directory = archetypes#' qa.cfg

        elif [[ -d "repoze" ]]; then
            sed -i 's#directory = src#directory = repoze#' qa.cfg

        elif [[ -d "plonetheme" ]]; then
            sed -i 's#directory = src#directory = plonetheme#' qa.cfg

        elif [[ -d "ZConfig" ]]; then
            sed -i 's#directory = src#directory = ZConfig#' qa.cfg

        elif [[ -d "txtfilter" ]]; then
            sed -i 's#directory = src#directory = txtfilter#' qa.cfg

        elif [[ -d "transaction" ]]; then
            sed -i 's#directory = src#directory = transaction#' qa.cfg

        elif [[ -d "borg" ]]; then
            sed -i 's#directory = src#directory = borg#' qa.cfg

        else
            echo "ooops on $pkg";
        fi

        $PYTHON27 bootstrap.py -c qa.cfg
        bin/buildout -c qa.cfg
        ./bin/code-analysis > qa.txt
        sed -i 's#^#src/'"$pkg"'/#' qa.txt  # fix path for jenkins violations plugin
        cat qa.txt >> ../../qa.txt
        cd ..

    fi
done
