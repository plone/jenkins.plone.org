#!/bin/sh

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

pip install -Ur requirements.txt
buildout buildout:git-clone-depth=1 -c py3.cfg

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=chrome
export ROBOTSUITE_PREFIX=ROBOT

alias xvfb-wrap="xvfb-run -a --server-args='-screen 0 1920x1200x24'"

# All tests without Robot
xvfb-wrap bin/test --all --xml -t '!ROBOT' || return_code="$?"
# All tests with Robot
xvfb-wrap bin/test --all --xml -t ROBOT || return_code="$?"

if [ "$return_code" = 'all_right' ]; then
    return_code="$?"
fi

# Update GitHub pull request status
python templates/pr-update-status-py3.py

# Keep tests return code
exit "$return_code"
