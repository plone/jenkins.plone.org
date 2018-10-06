#!/bin/sh

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

pip install -r requirements.txt

if [ "{plone-version}" = "4.3" ]; then
    buildout buildout:git-clone-depth=1 -c jenkins.cfg
else
    buildout buildout:git-clone-depth=1 -c core.cfg
fi

return_code="all_right"

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER='chrome'

if [ "{plone-version}" = "4.3" ]; then
    xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/jenkins-alltests -1 || return_code=$?
else
    xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/alltests --xml --all || return_code=$?
    xvfb-run -a --server-args='-screen 0 1920x1200x24' bin/alltests-at --xml || return_code=$?
fi

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Update GitHub pull request status
python templates/pr-update-status.py

# Keep tests return code
exit $return_code
