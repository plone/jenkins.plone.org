#!/bin/bash
if [ "{plone-version}" = "4.3" ]; then
    sed -i 's/    buildout.dumppickedversions/    buildout.dumppickedversions\ngit-clone-depth = 100/' core.cfg
    python bootstrap.py
    bin/buildout -c experimental/i18n.cfg install i18ndude i18n i18n-update-all
else
    sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
    pip install -r requirements.txt
    buildout -c experimental/i18n.cfg install i18ndude i18n i18n-update-all
fi

./bin/i18n-update-all

cd src/plone.app.locales/plone/app/locales/locales
mkdir reports

../../../../../../bin/i18ndude list -p plone > reports/plone.txt
../../../../../../bin/i18ndude list -p atcontenttypes  > reports/atcontenttypes.txt
../../../../../../bin/i18ndude list -p atreferencebrowserwidget  > reports/atreferencebrowserwidget.txt
../../../../../../bin/i18ndude list -p cmfeditions  > reports/cmfeditions.txt
../../../../../../bin/i18ndude list -p cmfplacefulworkflow  > reports/cmfplacefulworkflow.txt
../../../../../../bin/i18ndude list -p plonefrontpage  > reports/plonefrontpage.txt
../../../../../../bin/i18ndude list -p plonelocales  > reports/plonelocales.txt

if [ "{plone-version}" = "4.3" ]; then
    ../../../../../../bin/i18ndude list -p linguaplone  > reports/linguaplone.txt
    ../../../../../../bin/i18ndude list -p passwordresettool  > reports/passwordresettool.txt
else
    ../../../../../../bin/i18ndude list -p widgets  > reports/widgets.txt
fi
