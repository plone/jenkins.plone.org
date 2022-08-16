#!/bin/sh

PYTHON_VERSION="{py}"
/srv/python${{PYTHON_VERSION}}/bin/python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER="headlesschrome"
export ROBOTSUITE_PREFIX=ONLYROBOT

if [ "{plone-version}" = "5.2" ]; then
    export ROBOT_BROWSER="chrome"
fi

bin/test -t ONLYROBOT --all --xml
