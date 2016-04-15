#!/bin/bash
# buildout, core and AT tests
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
$PYTHON27 bootstrap.py --setuptools-version 21.0.0 -c {buildout}
./marker.sh set $$
bin/buildout -c {buildout}
./marker.sh release

return_code="all_right"

bin/alltests --xml --all || return_code=$?
bin/alltests-at --xml || return_code=$?

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Update GitHub pull request status
$PYTHON27 templates/pr-update-status.py

# Keep tests return code
exit $return_code
