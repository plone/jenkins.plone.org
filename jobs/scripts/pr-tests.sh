#!/bin/bash

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

pip install -r requirements.txt

if [ "{plone-version}" = "4.3" ]; then
    buildout -c jenkins.cfg
else
    buildout -c core.cfg
fi

return_code="all_right"

ROBOT_BROWSER="chrome"
if [ "{plone-version}" = "4.3" ]; then
    bin/jenkins-alltests -1 || return_code=$?
else
    bin/alltests --xml --all || return_code=$?
    bin/alltests-at --xml || return_code=$?
fi

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Update GitHub pull request status
python templates/pr-update-status.py

# Keep tests return code
exit $return_code
