#!/bin/bash
set -x

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

uv run -p {py} --with-requirements requirements.txt buildout buildout:git-clone-depth=1 -c buildout.cfg

return_code="all_right"

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER='headlesschrome'
export ROBOTSUITE_PREFIX=ONLYROBOT
export PYTHONWARNINGS='ignore'

export PLAYWRIGHT_BROWSERS_PATH='/home/jenkins/robot-browsers/'

# enable nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

bin/rfbrowser init chromium
# All tests without Robot
bin/test --all --xml . -t '!ONLYROBOT' || return_code="$?"
# All tests with Robot
bin/test --all --xml . -t ONLYROBOT || return_code="$?"

if [ "$return_code" = "all_right" ]; then
    return_code="$?"
fi

# Update GitHub pull request status
uv run --with pygithub==1.56 templates/pr-update-status-py3.py

# Keep tests return code
exit "$return_code"
