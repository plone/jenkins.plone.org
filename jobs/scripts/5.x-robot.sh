#!/bin/sh
pip install -r requirements.txt

BUILDOUT="core.cfg"
SCRIPT="bin/alltests"

if [ "{plone-version}" = "5.2" ]; then
    BUILDOUT="buildout.cfg"
    SCRIPT="bin/test"
    REALBROWSER="chrome"
fi
if [ "{plone-version}" = "6.0" ]; then
    BUILDOUT="buildout.cfg"
    SCRIPT="bin/test"
    REALBROWSER="headlesschrome"
fi

buildout buildout:git-clone-depth=1 -c ${{BUILDOUT}}

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=REALBROWSER
export ROBOTSUITE_PREFIX=ONLYROBOT

if [ "{plone-version}" = "5.2" ]; then
    xvfb-run -a --server-args='-screen 0 1920x1200x24' ${{SCRIPT}} -t ONLYROBOT --all --xml
else
    ${{SCRIPT}} -t ONLYROBOT --all --xml
fi