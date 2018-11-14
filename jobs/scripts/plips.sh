#!/bin/sh
pip install -r requirements.txt

buildout buildout:git-clone-depth=1 -c {buildout}

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=chrome

xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/test --xml --all
