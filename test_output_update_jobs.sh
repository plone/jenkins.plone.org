#!/usr/bin/env bash
jenkins-jobs --conf jobs/config.ini.in test jobs/jobs.yml --config-xml -o output
