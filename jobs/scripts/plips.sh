#!/bin/sh
set -x

pip install -r requirements.txt

buildout buildout:git-clone-depth=1 -c {buildout}

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=headlesschrome
export PYTHONWARNINGS='ignore'

bin/test --xml --all
