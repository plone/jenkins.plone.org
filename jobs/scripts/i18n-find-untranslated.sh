#!/usr/bin/env bash
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c experimental/i18n.cfg install i18n-find-untranslated i18ndude
export PYTHONIOENCODING=utf-8
bin/i18n-find-untranslated details > missing.txt
