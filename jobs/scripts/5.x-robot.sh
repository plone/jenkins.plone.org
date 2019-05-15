#!/bin/sh
pip install -r requirements.txt

BUILDOUT="core.cfg"
SCRIPT="bin/alltests"

if [ "{plone-version}" = "5.2" ]; then
    BUILDOUT="buildout.cfg"
    SCRIPT="bin/test"
fi

buildout buildout:git-clone-depth=1 -c ${{BUILDOUT}}

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER={browser}
export ROBOTSUITE_PREFIX=ONLYROBOT

${{SCRIPT}} -t ONLYROBOT --all --xml
