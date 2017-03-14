#!/bin/bash
MARKER_FILE=~/BUILDOUT-RUNNING
MAX_TRIES=20
SEC=10
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
    # Check if the marker file exists and if the stored pid belongs to
    # an active process.  If so, wait and try again.  For safety, if
    # this takes too long, we take over: maybe the server has
    # restarted, this file is still lying around, and it contains a
    # pid that belongs to a completely different process that will
    # remain active a long time.
    PREV_PID="UNKNOWN"
    while true; do
        PID_CHANGED=0
        for try in $(seq $MAX_TRIES); do
            echo "Try $try"
            if test -e $MARKER_FILE; then
                CURRENT_PID=$(cat $MARKER_FILE)
                echo "Marker file $MARKER_FILE exists for PID $CURRENT_PID."
                # If this is not the first try and the pid has changed,
                # then another script was lucky and sneaked in.  So we
                # start looping fresh.
                if test "$PREV_PID" != "UNKNOWN" && test "$PREV_PID" != "$CURRENT_PID"; then
                    echo "PID has changed from $PREV_PID to $CURRENT_PID, starting over."
                    PREV_PID="$CURRENT_PID"
                    PID_CHANGED=1
                    break
                fi
                PREV_PID="$CURRENT_PID"
                if ! test $(pgrep -F $MARKER_FILE); then
                    echo "PID $CURRENT_PID is no longer running. We will take over."
                    rm $MARKER_FILE
                    break
                else
                    echo "Waiting $SEC seconds..."
                    sleep $SEC
                fi
            else
                echo "Marker file $MARKER_FILE not found."
                break
            fi
        done
        if test $PID_CHANGED -eq 1; then
            # start over
            continue
        fi
        if test $try -eq $MAX_TRIES; then
            echo "Waited $MAX_TRIES times, lost patience, we take over."
        fi
        break
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
