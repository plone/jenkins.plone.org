# -*- coding: utf-8 -*-
from github import Github
from github.GithubException import BadCredentialsException
from github.GithubException import UnknownObjectException

import fileinput
import os
import re
import sys


class AddonInfo(object):

    addon_name = ''
    addon_url = ''
    addon_branch = 'master'
    in_known_github_org = False
    github_org = ''

    github_api_key = ''
    github = None
    latest_commit = ''

    known_github_orgs = (
        ('github.com/collective', 'collective', ),
        ('github.com/plone', 'plone', ),
    )

    def process_input(self):
        self.get_addon_details()
        if self.in_known_github_org:
            self.get_gitub_api_key()
            self.github = Github(self.github_api_key)
            self.latest_commit = self.get_latest_commit()

    def get_addon_details(self):
        try:
            self.addon_url = os.environ['ADDON_URL']
        except KeyError:
            print(
                '\n\n\n'
                'You seem to forgot to add an add-on URL on the '
                '"Build with parameters" form!'
                '\n\n\n'
            )
            sys.exit(1)

        try:
            self.addon_branch = os.environ['ADDON_BRANCH']
        except KeyError:
            self.addon_branch = None

        if self.addon_branch is None:
            self.addon_branch = 'master'

        for org_data in self.known_github_orgs:
            if org_data[0] in self.addon_url:
                self.in_known_github_org = True
                self.github_org = org_data[1]
                break

        self.addon_name = self._get_addon_name()

    def _get_addon_name(self):
        url = self.addon_url
        if self.addon_url.endswith('.git'):
            url = self.addon_url[:-4]  # Remove the `.git` suffix
        matches = re.search(r'/([\d\w.\-_]+?)$', url)
        if matches:
            return matches.groups()[0]
        else:
            print(
                '\n\n\n'
                'Could not get the add-on name out of the URL, '
                'be sure that the last part of the URL is the add-on name.'
                '\n\n\n'
            )
            sys.exit(1)

    def get_gitub_api_key(self):
        try:
            self.github_api_key = os.environ['GITHUB_API_KEY']
        except KeyError:
            print(
                '\n\n\n'
                'GITHUB_API_KEY is missing, this job can not run without it. '
                '\n'
                'Please contact the testing team: '
                'https://github.com/orgs/plone/teams/testing-team'
                '\n'
                'Fill an issue as well: '
                'https://github.com/plone/jenkins.plone.org/issues/new'
                '\n\n\n'
            )
            sys.exit(1)

    def get_latest_commit(self):
        try:
            g_organization = self.github.get_organization(self.github_org)
            g_repository = g_organization.get_repo(self.addon_name)
            g_branch = g_repository.get_branch(self.addon_branch)
            return g_branch.commit.sha
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
                'Error on trying to get info from add-on URL %s'
                '\n'
                'Double check that the provided information is valid.'
                '\n\n\n'
            )
            print(msg % (self.addon_url, self.github_org))
            sys.exit(1)

    def write_properties_file(self):
        print('add-on name: ' + self.addon_name)
        print('add-on URL: ' + self.addon_url)
        print('add-on branch: ' + self.addon_branch)
        print('add-on in github: ' + str(self.in_known_github_org))
        print('add-on github org: ' + self.github_org)
        print('add-on latest commit: ' + self.latest_commit)
        msg = (
            'ADDON_NAME = {0}\n'
            'ADDON_URL = {1}\n'
            'ADDON_BRANCH = {2}\n'
            'REPORT_ON_GITHUB = {3}\n'
            'GITHUB_LATEST_COMMIT = {4}\n'
        )
        data = [
            self.addon_name,
            self.addon_url,
            self.addon_branch,
            str(self.in_known_github_org),
            self.latest_commit,
        ]

        with open('vars.properties', 'w') as f:
            f.write(msg.format(*data))

    def add_package_to_buildout(self):
        # add the package on the checkouts
        with open('checkouts.cfg', 'a') as myfile:
            myfile.write('    {0}'.format(self.addon_name))

        # add the package on sources
        with open('sources.cfg', 'a') as myfile:
            myfile.write('{0} = git {1} rev={2}'.format(
                self.addon_name,
                self.addon_url,
                self.latest_commit,
            ))

        # add the package to tests.cfg
        for line in fileinput.input('tests.cfg', inplace=True):
            if line.find('Products.CMFPlone [test]') != -1:
                # TODO(gforcada): what if the add-on needs some extras??
                line = '    Products.CMFPlone [test]\n    {0}\n'
                line = line.format(self.addon_name)
            sys.stdout.write(line)


add_on = AddonInfo()
add_on.process_input()
add_on.add_package_to_buildout()
add_on.write_properties_file()
"""
RUN TEST
- report with a comment if REPORT_ON_GITHUB is true
  - if tests pass and no trove classifier is found, warn about it

REPORT BY EMAIL
  - if tests pass and no trove classifier is found, warn about it
"""
