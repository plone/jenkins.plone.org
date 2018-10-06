#!/bin/sh
if [ "{plone-version}" = "4.3" ]; then
    python bootstrap.py
    bin/buildout buildout:git-clone-depth=1 -c experimental/i18n.cfg install i18ndude i18n i18n-update-all
else
    pip install -Ur requirements.txt
    buildout buildout:git-clone-depth=1 -c experimental/i18n.cfg install i18ndude i18n i18n-update-all
fi

./bin/i18n-update-all

cd src/plone.app.locales/plone/app/locales/locales || exit 1
mkdir reports

export PYTHONIOENCODING=utf-8

alias i18ndude '../../../../../../bin/i18ndude'

i18ndude list -p plone > reports/plone.txt
i18ndude list -p atcontenttypes  > reports/atcontenttypes.txt
i18ndude list -p atreferencebrowserwidget  > reports/atreferencebrowserwidget.txt
i18ndude list -p cmfeditions  > reports/cmfeditions.txt
i18ndude list -p cmfplacefulworkflow  > reports/cmfplacefulworkflow.txt
i18ndude list -p plonefrontpage  > reports/plonefrontpage.txt
i18ndude list -p plonelocales  > reports/plonelocales.txt

if [ "{plone-version}" = "4.3" ]; then
    i18ndude list -p linguaplone  > reports/linguaplone.txt
    i18ndude list -p passwordresettool  > reports/passwordresettool.txt
else
    i18ndude list -p widgets  > reports/widgets.txt
fi
