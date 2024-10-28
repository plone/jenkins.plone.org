#!/bin/bash
set -x

PYTHON_VERSION="{py}"
PLONE_VERSION="{plone-version}"

/srv/python${{PYTHON_VERSION}}/bin/python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER="headlesschrome"
export ROBOTSUITE_PREFIX=ONLYROBOT
export PYTHONWARNINGS='ignore'

if [[ "${{PLONE_VERSION}}" == 6* ]]; then
  export PLAYWRIGHT_BROWSERS_PATH='/home/jenkins/robot-browsers/'

  # enable nvm
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

  bin/rfbrowser init chromium
  bin/test -t ONLYROBOT --all --xml .
else
  bin/test -t ONLYROBOT --all --xml
fi
