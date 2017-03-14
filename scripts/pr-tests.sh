#!/bin/bash
if [ "{plone-version}" = "4.3" ]; then
    $PYTHON27 bootstrap.py -c jenkins.cfg
else
    $PYTHON27 bootstrap.py --setuptools-version 21.0.0 -c jenkins.cfg
fi
if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

./marker.sh set $$
bin/buildout -c jenkins.cfg
./marker.sh release

return_code="all_right"

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
$PYTHON27 templates/pr-update-status.py

# Keep tests return code
exit $return_code
