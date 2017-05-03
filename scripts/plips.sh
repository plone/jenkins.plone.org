#!/bin/bash
# buildout, core and AT tests
sed -i 's/    mr.developer/    mr.developer\ngit-clone-depth = 100/' core.cfg
$PYTHON27 bootstrap.py --setuptools-version 33.1.1 --buildout-version 2.8.0 -c {buildout}
bin/buildout -c {buildout}

return_code="all_right"

bin/alltests --xml --all || return_code=$?
bin/alltests-at --xml || return_code=$?

if [ $return_code = "all_right" ]; then
    return_code=$?
fi

# Keep tests return code
exit $return_code
