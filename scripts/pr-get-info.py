# -*- coding: utf-8 -*-
import fileinput
import json
import os
import re
import sys
import urllib2

pull_request_urls = os.environ['PULL_REQUEST_URL']

PKG_RE = r'^{0}\s.*'
SOURCE_RE = r'{0} = git git://github.com/{1}/{0}.git branch={2}'

PKGS = []
COREDEV = 0

for i, pr in enumerate(pull_request_urls.split()):
    github_api_call = pr.replace('github.com', 'api.github.com/repos')
    github_api_call = github_api_call.replace('/pull/', '/pulls/')

    response = urllib2.urlopen(github_api_call)
    json_data = json.loads(response.read())

    org, branch = json_data['head']['label'].split(':')
    pkg = json_data['base']['repo']['name']

    if pkg != 'buildout.coredev':
        PKGS.append(pkg)
        for line in fileinput.input('sources.cfg', inplace=True):
            if line.find(pkg) != -1:
                line = re.sub(
                    PKG_RE.format(pkg),
                    SOURCE_RE.format(pkg, org, branch),
                    line
                )
            sys.stdout.write(line)
    else:
        COREDEV = 1

with open('vars.properties', 'w') as f:
    f.write(u'PKGS = {0}\n'.format(' '.join(PKGS)))
    f.write(u'COREDEV = {0}\n'.format(COREDEV))
