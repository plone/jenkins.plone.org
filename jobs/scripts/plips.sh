#!/bin/bash
# buildout, core and AT tests
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
pip install -r requirements.txt
buildout -c {buildout}

return_code="all_right"
ROBOT_BROWSER=chrome

bin/alltests --xml --all || return_code=$?
bin/alltests-at --xml || return_code=$?

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Keep tests return code
exit $return_code
