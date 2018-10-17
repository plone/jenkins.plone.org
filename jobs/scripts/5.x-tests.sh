#!/bin/sh
pip install -r requirements.txt

BUILDOUT="core.cfg"
SCRIPT="bin/alltests"

if [ "{plone-version}" = "5.2" ]; then
    BUILDOUT="buildout-py3.cfg"
    SCRIPT="bin/test"

    if [ "{py}" = "2.7" ]; then
        BUILDOUT="buildout-py2.cfg"
    fi
fi

buildout buildout:git-clone-depth=1 -c ${{BUILDOUT}}
${{SCRIPT}} --xml
