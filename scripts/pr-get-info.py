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
job_name = os.environ['JOB_NAME']

g = Github(github_api_key)

for pr in pull_request_urls.split():
    org, plone_repo, pr_number = re.search(PR_RE, pr).groups()

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
        g_repo = g_org.get_repo(plone_repo)
    except UnknownObjectException:
        msg = (
            '\n\n\n'
            'Error on trying to get info from Pull Request %s'
            '\n'
            'The repository "%s" does not seem to exist.'
            '\n\n\n'
        )
        print(msg % (pr, plone_repo))
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

    # get the user where the pull request comes from
    user = g_pr.head.repo.owner.login

    # add a 'pending' status
    last_commit = g_pr.get_commits().reversed[0]
    try:
        last_commit.create_status(
            u'pending',
            target_url=build_url,
            description='Job started, wait until it finishes',
            context='Plone Jenkins CI - {0}'.format(job_name),
        )
    except UnknownObjectException:
        msg = (
            '\n\n\n'
            'Could not update Pull Request %s'
            '\n\n\n'
        )
        print(msg % pr)

    if plone_repo != 'buildout.coredev':
        # export the packages so it can be reported by mail
        PKGS.append(plone_repo)
        # change the package source
        for line in fileinput.input('sources.cfg', inplace=True):
            if line.find(plone_repo) != -1:
                line = re.sub(
                    PKG_RE.format(plone_repo),
                    SOURCE_RE.format(plone_repo, user, branch),
                    line
                )
            sys.stdout.write(line)

        # add the package on the checkouts
        with open('checkouts.cfg', 'a') as myfile:
            myfile.write('    {0}'.format(plone_repo))
    else:
        COREDEV = 1

with open('vars.properties', 'w') as f:
    f.write(u'PKGS = {0}\n'.format(' '.join(PKGS)))
    f.write(u'COREDEV = {0}\n'.format(COREDEV))
    if COREDEV == 1:
        f.write(u'PKGS = \n')
        f.write(u'BRANCH = {0}\n'.format(branch))
