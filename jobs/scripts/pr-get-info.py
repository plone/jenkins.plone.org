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
BRANCH = ''


def error(message):
    print(
        '\n\n\n'
        f'{message}'
        '\n'
        'Please contact the testing team: '
        'https://github.com/orgs/plone/teams/testing-team'
        '\n'
        'Fill an issue as well: '
        'https://github.com/plone/jenkins.plone.org/issues/new'
        '\n\n\n'
    )
    sys.exit(1)


def api_key():
    try:
        return os.environ['GITHUB_API_KEY']
    except KeyError:
        error('GITHUB_API_KEY does not exist, pull request job can not run. ')


def pull_requests():
    try:
        return os.environ['PULL_REQUEST_URL'].split()
    except KeyError:
        error(
            'You seem to forgot to add a pull request URL on the '
            '"Build with parameters" form!'
        )


class PullRequest:

    def __init__(self, github, job_name, build_url):
        self.g = github
        self.job_name = job_name
        self.build_url = build_url

    def __call__(self, url):
        self.url = url

        data = re.search(PR_RE, url).groups()
        self.org, self.repo, self.pr_number = data

        self._pr_number()
        self._pr_org()
        self._pr_repo()
        self._pr_itself()
        self._user_and_branch()
        self._add_pending_status()

        if self.repo != 'buildout.coredev':
            self._no_coredev_pkg()
        else:
            global COREDEV
            global BRANCH
            COREDEV = 1
            BRANCH = self.branch

    def _pr_number(self):
        try:
            self.pr_number = int(self.pr_number)
        except ValueError:
            error(
                f'Error on trying to get info from Pull Request {self.url}'
                '\n'
                f'The pull request number "{self.pr_number}" is not a number!'
            )

    def _pr_org(self):
        """Get the pull request organization it belongs to"""
        try:
            self.g_org = self.g.get_organization(self.org)
        except BadCredentialsException:
            error('The API key used seems to not be valid any longer.')
        except UnknownObjectException:
            error(
                f'Error on trying to get info from Pull Request {self.url}'
                '\n'
                f'The organization "{self.org}" does not seem to exist.'
            )

    def _pr_repo(self):
        """The repo where the pull request is from"""
        try:
            self.g_repo = self.g_org.get_repo(self.repo)
        except UnknownObjectException:
            error(
                f'Error on trying to get info from Pull Request {self.url}'
                '\n'
                f'The repository "{self.repo}" does not seem to exist.'
            )

    def _pr_itself(self):
        """The pull request itself"""
        try:
            self.g_pr = self.g_repo.get_pull(self.pr_number)
        except UnknownObjectException:
            error(
                f'Error on trying to get info from Pull Request {self.url}'
                '\n'
                f'The pull request num "{self.pr_number}" does not seem to exist.'
            )

    def _user_and_branch(self):
        # get the branch
        self.branch = self.g_pr.head.ref

        # get the user where the pull request comes from
        self.user = self.g_pr.head.repo.owner.login

    def _add_pending_status(self):
        last_commit = self.g_pr.get_commits().reversed[0]
        try:
            last_commit.create_status(
                u'pending',
                target_url=self.build_url,
                description='Job started, wait until it finishes',
                context=f'Plone Jenkins CI - {self.job_name}',
            )
        except UnknownObjectException:
            error(f'Could not update Pull Request {self.url}')

    def _no_coredev_pkg(self):
        # export the packages so it can be reported by mail
        PKGS.append(self.repo)
        # change the package source
        with fileinput.input('sources.cfg', inplace=True) as file_handler:
            for line in file_handler:
                if line.find(self.repo) != -1:
                    line = re.sub(
                        PKG_RE.format(self.repo),
                        SOURCE_RE.format(self.repo, self.user, self.branch),
                        line,
                    )
                sys.stdout.write(line)

        # add the package on the checkouts
        with open('checkouts.cfg', 'a') as myfile:
            myfile.write(f'    {self.repo}\n')


def write_properties_file():
    with open('vars.properties', 'w') as vars_file:
        packages = ' '.join(PKGS)
        vars_file.write(f'PKGS = {packages}\n')
        vars_file.write(f'COREDEV = {COREDEV}\n')
        if COREDEV == 1:
            vars_file.write('PKGS = \n')
            vars_file.write(f'BRANCH = {BRANCH}\n')


def main():
    github_api_key = api_key()
    pull_request_urls = pull_requests()

    build_url = os.environ['BUILD_URL']
    job_name = os.environ['JOB_NAME']
    g = Github(github_api_key)

    pull_request_handler = PullRequest(g, job_name, build_url)
    for pr in pull_request_urls:
        pull_request_handler(pr)

    write_properties_file()


main()
