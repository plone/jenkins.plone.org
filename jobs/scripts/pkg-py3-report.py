# -*- coding: utf-8 -*-
from github import Github
from github.GithubException import BadCredentialsException
from github.GithubException import UnknownObjectException

import os
import re
import sys


tests_folder = 'parts/test/testreports'
job_run_successfully = True

# bare basic way to know if there was any test failure
try:
    files = [f for f in os.listdir(tests_folder)]
except OSError:
    files = []
    job_run_successfully = False


for f in files:
    with open('{{0}}/{{1}}'.format(tests_folder, f)) as xml_file:
        first_line = xml_file.read().split('\n')[0]

        failures = True
        if first_line.find('failures="0"') != -1:
            failures = False

        errors = True
        if first_line.find('errors="0"') != -1:
            errors = False

        if failures or errors:
            job_run_successfully = False
            break

if job_run_successfully:
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

header = '@%s Jenkins CI reporting about python 3.5 compatibility' % author
first_line = 'See the full report here: %stestReport' % build_url
footer = 'Note that it can be a false positive if you are working on a ' \
         'branch that is not up-to-date with master (which should be ' \
         'compatible already).'
comment = '%s\n%s\n%s' % (
    header,
    first_line,
    footer
)
g_commit.create_comment(
    body=comment
)

# if a comment was sent is because the tests did not pass
# tell jenkins that the build fail
sys.exit(1)
