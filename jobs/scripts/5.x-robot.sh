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

xvfb-run -a --server-args='-screen 0 1920x1200x24' ${{SCRIPT}} -t ONLYROBOT --all --xml
