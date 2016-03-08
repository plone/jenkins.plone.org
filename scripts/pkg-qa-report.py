# -*- coding: utf-8 -*-
from github import Github
from github.GithubException import BadCredentialsException
from github.GithubException import UnknownObjectException

import os
import re
import sys

with open('parts/code-analysis/flake8.log') as flake8_log:
    flake8_errors = flake8_log.read()

if flake8_errors == '':
    print('No flake8 errors found, nothing to report')
    sys.exit(0)


try:
    github_api_key = os.environ['GITHUB_API_KEY']
except KeyError:
    print(
        '\n\n\n'
        'GITHUB_API_KEY does not exist, package QA job can not run. '
        '\n'
        'Please contact the testing team: '
        'https://github.com/orgs/plone/teams/testing-team'
        '\n'
        'Fill an issue as well: '
        'https://github.com/plone/jenkins.plone.org/issues/new'
        '\n\n\n'
    )
    sys.exit(1)

GIT_URL_RE = r'github\.com/(.*)/(.*).git'

build_url = os.environ['BUILD_URL']
job_name = os.environ['JOB_NAME']
git_url = os.environ['GIT_URL']
git_commit = os.environ['GIT_COMMIT']

g = Github(github_api_key)

try:
    org, repo = re.search(GIT_URL_RE, git_url).groups()
except AttributeError, ValueError:
    msg = (
        '\n\n\n'
        'Error on trying to get info from the git URL %s'
        '\n\n\n'
    )
    print(msg % git_url)
    sys.exit(1)

# get the organization
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
        'Error: the organization "%s" does not seem to exist.'
        '\n\n\n'
    )
    print(msg % org)
    sys.exit(1)

# get the repo
try:
    g_repo = g_org.get_repo(repo)
except UnknownObjectException:
    msg = (
        '\n\n\n'
        'Error: the repository "%s" does not seem to exist.'
        '\n\n\n'
    )
    print(msg % repo)
    sys.exit(1)

# get the commit
try:
    g_commit = g_repo.get_commit(git_commit)
except UnknownObjectException:
    msg = (
        '\n\n\n'
        'Error: the commit "%s" does not seem to exist.'
        '\n\n\n'
    )
    print(msg % git_commit)
    sys.exit(1)


try:
    author = g_commit.author.login
except AttributeError:
    # If the user does not exist on github,
    # get the username of the commit
    author = g_commit.commit.author.name

header = '@%s Jenkins CI reporting about code analysis' % author
first_line = 'See the full report here: %sviolations' % build_url
footer = 'Follow [these instructions](https://github.com/plone/jenkins.plone.org/blob/master/docs/source/run-qa-on-package.rst) to reproduce it locally.'
comment = '%s\n%s\n```\n%s```\n%s' % (
    header,
    first_line,
    flake8_errors,
    footer
)
g_commit.create_comment(
    body=comment
)
