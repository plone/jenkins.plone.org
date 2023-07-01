#!/bin/sh

PYTHON_VERSION="{py}"
PLONE_VERSION="{plone-version}"

/srv/python${{PYTHON_VERSION}}/bin/python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER="headlesschrome"
export ROBOTSUITE_PREFIX=ONLYROBOT

if [[ "${{PLONE_VERSION}}" == 6* ]]; then
  export PLAYWRIGHT_BROWSERS_PATH='/home/jenkins/robot-browsers/'

  bin/rfbrowser init
fi
bin/test -t ONLYROBOT --all --xml
