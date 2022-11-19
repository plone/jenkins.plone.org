#!/bin/sh

python_version="{py}"
/srv/python${{python_version}}/bin/python3 -m venv venv
. venv/bin/activate

if [ "$COREDEV" = "1" ]; then
    # TODO(gforcada): allow to test remote branches (i.e. branches not in github.com/plone/buildout.coredev)
    git checkout $BRANCH
fi

pip install pygithub==1.56
pip install -r requirements.txt
buildout buildout:git-clone-depth=1 -c buildout.cfg

return_code="all_right"

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER='headlesschrome'
export ROBOTSUITE_PREFIX=ONLYROBOT
export PYTHONWARNINGS='ignore'

# All tests without Robot
bin/test --all --xml -t '!ONLYROBOT' || return_code="$?"
# All tests with Robot
bin/test --all --xml -t ONLYROBOT || return_code="$?"

if [ "$return_code" = "all_right" ]; then
    return_code="$?"
fi

# Update GitHub pull request status
python templates/pr-update-status-py3.py

# Keep tests return code
exit "$return_code"
