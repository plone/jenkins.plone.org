#!/bin/sh

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg

return_code="all_right"

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER='headlesschrome'
export PYTHONWARNINGS='ignore'

# switch to headless chrome
#xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/test --all --xml || return_code=$?

bin/test --all --xml

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Update GitHub pull request status
python templates/pr-update-status-py3.py

# Keep tests return code
exit $return_code
