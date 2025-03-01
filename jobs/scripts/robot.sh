#!/bin/bash
set -x

uv run -p {py} --with-requirements requirements.txt buildout buildout:git-clone-depth=1 -c buildout.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER="headlesschrome"
export ROBOTSUITE_PREFIX=ONLYROBOT
export PYTHONWARNINGS='ignore'

export PLAYWRIGHT_BROWSERS_PATH='/home/jenkins/robot-browsers/'

# enable nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

bin/rfbrowser init chromium
bin/test -t ONLYROBOT --all --xml .
