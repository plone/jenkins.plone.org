#!/bin/bash

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

pip install -r requirements.txt
buildout -c py3.cfg

return_code="all_right"
./bin/test --xml -vvv  || return_code=$?

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Update GitHub pull request status
python templates/pr-update-status.py

# Keep tests return code
exit $return_code
