#!/bin/sh
# run buildout and tests
{pybinary} bootstrap.py
bin/buildout buildout:git-clone-depth=1

export PATH="/usr/lib/chromium-browser:$PATH"
export ROBOT_BROWSER=chrome
export ROBOTSUITE_PREFIX=ROBOT

alias xvfb-wrap="xvfb-run -a --server-args='-screen 0 1920x1200x24'"

return_code='all_right'

# Archetypes tests without Robot
xvfb-wrap bin/jenkins-alltests-at --all --xml -t '!ROBOT' || return_code="$?"
# Archetypes tests with only Robot
xvfb-wrap bin/jenkins-alltests-at --all --xml -t ROBOT || return_code="$?"

# Dexterity tests without Robot
xvfb-wrap bin/jenkins-alltests --all --xml -t '!ROBOT' || return_code="$?"
# Dexterity tests with only Robot
xvfb-wrap bin/jenkins-alltests --all --xml -t ROBOT || return_code="$?"

if [ $return_code = 'all_right' ]; then
    exit "$?"
fi

exit "$return_code"
