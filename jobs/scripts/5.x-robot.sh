#!/bin/sh
pip install -Ur requirements.txt
buildout buildout:git-clone-depth=1 -c core.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER={browser}
export ROBOTSUITE_PREFIX=ROBOT

alias xvfb-wrap="xvfb-run -a --server-args='-screen 0 1920x1200x24'"

xvfb-wrap bin/alltests --all --xml -t ROBOT
