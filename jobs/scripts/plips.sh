#!/bin/sh
set -x

PYTHON_VERSION="{py}"

/srv/python${{PYTHON_VERSION}}/bin/python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt

buildout buildout:git-clone-depth=1 -c {buildout}

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER="headlesschrome"
export ROBOTSUITE_PREFIX=ONLYROBOT
export PYTHONWARNINGS='ignore'

export PLAYWRIGHT_BROWSERS_PATH='/home/jenkins/robot-browsers/'
bin/rfbrowser init

bin/test --xml . --all
