#!/bin/sh

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

pip install -r requirements.txt

if [ "{plone-version}" = "4.3" ]; then
    buildout buildout:git-clone-depth=1 -c jenkins.cfg
elif [ "{plone-version}" = "5.2" ]; then
    buildout buildout:git-clone-depth=1 -c buildout.cfg
else
    buildout buildout:git-clone-depth=1 -c core.cfg
fi

return_code="all_right"

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER='headlesschrome'

if [ "{plone-version}" = "4.3" ]; then
    bin/jenkins-alltests -1 || return_code=$?
elif [ "{plone-version}" = "5.2" ]; then
    bin/test --all --xml || return_code=$?
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
