#!/bin/bash
# buildout, core and AT tests
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c {buildout}

return_code="all_right"
export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=chrome

xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/alltests --xml --all || return_code=$?
xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/alltests-at --xml || return_code=$?

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Keep tests return code
exit $return_code
