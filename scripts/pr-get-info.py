# -*- coding: utf-8 -*-
from github import Github
from github.GithubException import BadCredentialsException
from github.GithubException import UnknownObjectException

import fileinput
import os
import re
import sys


PKG_RE = r'^{0}\s.*'
SOURCE_RE = r'{0} = git git://github.com/{1}/{0}.git branch={2}'
PR_RE = r'https://github.com/(.*)/(.*)/pull/(.*)'

PKGS = []
COREDEV = 0

try:
    github_api_key = os.environ['GITHUB_API_KEY']
except KeyError:
    print(
        '\n\n\n'
        'GITHUB_API_KEY does not exist, pull request job can not run. '
        '\n'
        'Please contact the testing team: '
        'https://github.com/orgs/plone/teams/testing-team'
        '\n'
        'Fill an issue as well: '
        'https://github.com/plone/jenkins.plone.org/issues/new'
        '\n\n\n'
    )
    sys.exit(1)

try:
    pull_request_urls = os.environ['PULL_REQUEST_URL']
except KeyError:
    print(
        '\n\n\n'
        'You seem to forgot to add a pull request URL on the '
        '"Build with parameters" form!'
        '\n\n\n'
    )
    sys.exit(1)

build_url = os.environ['BUILD_URL']

g = Github(github_api_key)

for pr in pull_request_urls.split():
    org, repo, pr_number = re.search(PR_RE, pr).groups()

    try:
        pr_number = int(pr_number)
    except ValueError:
        msg = (
            '\n\n\n'
            'Error on trying to get info from Pull Request %s'
            '\n'
            'The pull request number "%s" is not a number!'
            '\n\n\n'
        )
        print(msg % (pr, pr_number))
        sys.exit(1)

    # get the pull request organization it belongs to
    try:
        g_org = g.get_organization(org)
    except BadCredentialsException:
        print(
            '\n\n\n'
            'The API key used seems to not be valid any longer.'
            '\n'
            'Please contact the testing team: '
            'https://github.com/orgs/plone/teams/testing-team'
            '\n'
            'Fill an issue as well: '
            'https://github.com/plone/jenkins.plone.org/issues/new'
            '\n\n\n'
        )
        sys.exit(1)
    except UnknownObjectException:
        msg = (
            '\n\n\n'
            'Error on trying to get info from Pull Request %s'
            '\n'
            'The organization "%s" does not seem to exist.'
            '\n\n\n'
        )
        print(msg % (pr, org))
        sys.exit(1)

    # the repo where the pull request is from
    try:
        g_repo = g_org.get_repo(repo)
    except UnknownObjectException:
        msg = (
            '\n\n\n'
            'Error on trying to get info from Pull Request %s'
            '\n'
            'The repository "%s" does not seem to exist.'
            '\n\n\n'
        )
        print(msg % (pr, repo))
        sys.exit(1)

    # the pull request itself
    try:
        g_pr = g_repo.get_pull(pr_number)
    except UnknownObjectException:
        msg = (
            '\n\n\n'
            'Error on trying to get info from Pull Request %s'
            '\n'
            'The pull request num "%s" does not seem to exist.'
            '\n\n\n'
        )
        print(msg % (pr, pr_number))
        sys.exit(1)

    # get the branch
    branch = g_pr.head.ref

    if repo != 'buildout.coredev':
        PKGS.append(repo)
        for line in fileinput.input('sources.cfg', inplace=True):
            if line.find(repo) != -1:
                line = re.sub(
                    PKG_RE.format(repo),
                    SOURCE_RE.format(repo, org, branch),
                    line
                )
            sys.stdout.write(line)
    else:
        COREDEV = 1

with open('vars.properties', 'w') as f:
    f.write(u'PKGS = {0}\n'.format(' '.join(PKGS)))
    f.write(u'COREDEV = {0}\n'.format(COREDEV))