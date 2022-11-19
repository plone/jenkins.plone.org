#!/bin/sh

pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER="chrome"
export ROBOTSUITE_PREFIX=ONLYROBOT

xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/test -t ONLYROBOT --all --xml
