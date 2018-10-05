#!/bin/sh
pip install -r requirements.txt
buildout buildout:git-clone-depth=50 -c py3.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=chrome

xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/test --all -j 6 --xml
