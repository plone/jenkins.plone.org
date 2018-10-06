#!/bin/sh
pip install -Ur requirements.txt
buildout buildout:git-clone-depth=1 -c py3.cfg

return_code="all_right"

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=chrome
export ROBOTSUITE_PREFIX=ROBOT

alias xvfb-wrap="xvfb-run -a --server-args='-screen 0 1920x1200x24'"

return_code='all_right'

# All tests without Robot
xvfb-wrap bin/test --all --xml -t '!ROBOT' || return_code="$?"
# All tests with Robot
xvfb-wrap bin/test --all --xml -t ROBOT || return_code="$?"

if [ "$return_code" = 'all_right' ]; then
    exit "$?"
fi

# Keep tests return code
exit "$return_code"
