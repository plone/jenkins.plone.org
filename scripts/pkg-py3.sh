#!/bin/bash
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/bootstrap.py -O bootstrap.py
wget https://raw.githubusercontent.com/plone/buildout.coredev/5.1/experimental/py3x-test.cfg -O test.cfg
sed -i 's#REPLACE_ME#{package}#' test.cfg
$PYTHON35 bootstrap.py --setuptools-version 21.0.0 -c test.cfg
bin/buildout -c test.cfg

# the script needs to ALWAYS exit without an error code,
# if not, the script that reports back to github will never run
# that script will take care of returning a suitable error code so that
# jenkins can, as well, report on the UI if a build was not successful
return_code="0"
bin/test || return_code=$?

exit 0
