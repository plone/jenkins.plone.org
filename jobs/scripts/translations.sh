#!/bin/sh
set -x

uv run -p {py} --with-requirements requirements.txt buildout buildout:git-clone-depth=1 -c experimental/i18n.cfg install i18ndude i18n i18n-update-all

./bin/i18n-update-all

cd src/plone.app.locales/plone/app/locales/locales || exit 1
mkdir reports

export PYTHONIOENCODING=utf-8

uv run -p {py} --with i18ndude i18ndude list -p plone > reports/plone.txt
uv run -p {py} --with i18ndude i18ndude list -p cmfeditions  > reports/cmfeditions.txt
uv run -p {py} --with i18ndude i18ndude list -p cmfplacefulworkflow  > reports/cmfplacefulworkflow.txt
uv run -p {py} --with i18ndude i18ndude list -p plonefrontpage  > reports/plonefrontpage.txt
uv run -p {py} --with i18ndude i18ndude list -p plonelocales  > reports/plonelocales.txt
uv run -p {py} --with i18ndude i18ndude list -p widgets  > reports/widgets.txt
