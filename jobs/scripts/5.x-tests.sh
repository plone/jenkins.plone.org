#!/bin/sh
pip install -r requirements.txt

BUILDOUT="core.cfg"
SCRIPT="bin/alltests"

if [ "{plone-version}" = "5.2" ]; then
    BUILDOUT="buildout.cfg"
    SCRIPT="bin/test"
fi

if [ "{plone-version}" = "6.0" ]; then
    BUILDOUT="buildout.cfg"
    SCRIPT="bin/test"
fi

buildout buildout:git-clone-depth=1 -c ${{BUILDOUT}}
${{SCRIPT}} --xml
