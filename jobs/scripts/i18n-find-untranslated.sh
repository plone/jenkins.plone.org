#!/bin/bash
if [ "{plone-version}" = "4.3" ]; then
    sed -i 's/    buildout.dumppickedversions/    buildout.dumppickedversions\ngit-clone-depth = 100/' core.cfg
    python bootstrap.py
    bin/buildout -c experimental/i18n.cfg install i18n-find-untranslated i18ndude
else
    sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
    pip install -r requirements.txt
    buildout -c experimental/i18n.cfg install i18n-find-untranslated i18ndude
fi

export PYTHONIOENCODING=utf-8
bin/i18n-find-untranslated details > missing.txt || echo 0
