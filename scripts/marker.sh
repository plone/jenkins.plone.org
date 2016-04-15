#!/bin/bash
MARKER_FILE=~/BUILDOUT-RUNNING
USAGE="
Goal: claim a marker file, run buildout, then unclaim the file.
This avoids issues building new packages when starting two Jenkins
jobs on the same node.  See
https://github.com/plone/jenkins.plone.org/issues/135

Marker file with process id: $MARKER_FILE

Usage:
$0 set <pid of calling script>
    Wait until marker file is no longer there
    or until the process with the id is no longer running,
    in case it got uncleanly broken off.
$0 release
    Cleanly release the marker file.
"

# 1. Wait for and set the marker.
if test $# -eq 2 && test "$1" == "set"; then
    # The second argument is the pid of the calling script.  In case
    # it is bogus, the marker will be stolen by the next calling
    # script, which is fine.
    PID="$2"
    while test -e $MARKER_FILE; do
        OTHER_PID=$(cat $MARKER_FILE)
        echo "Marker file $MARKER_FILE exists for PID $OTHER_PID."
        if ! test $(pgrep -F $MARKER_FILE); then
            echo "PID $OTHER_PID is no longer running. We will take over."
            rm $MARKER_FILE
        else
            echo "Waiting..."
            sleep 5
        fi
    done
    echo $PID > $MARKER_FILE
    echo "Created marker file $MARKER_FILE with our PID $PID."
    exit 0
fi

# 2. Remove the marker.
if test $# -eq 1 && test "$1" == "release"; then
    if test -e $MARKER_FILE; then
        rm -f $MARKER_FILE
        echo "Removed marker file $MARKER_FILE."
    else
        echo "Marker file $MARKER_FILE was already removed."
    fi
    exit 0
fi

# If you end up here, you have not called the script correctly.
echo "$USAGE"
exit 1
