# -*- coding: utf-8 -*-
from github import Github
import re
from netrc import netrc

white_list_re = [
    'plone.app.*',
    'plone.*',
]

black_list_re = [
    'plone.recipe.*',
    'plone.docker',
    'plone.jenkins_node',
    'plone.com.*',
    'plonejenkins.*',
    'plone-*',
    'plone.github.com',
    'plonedev.vagrant',
]


def get_github_api():
    login, account, password = netrc().authenticators('github.com')
    return Github(login, password)


def get_github_repo_list(gh=None):
    """ Return list of repo name we have to test in Jenkins
    """
    if not gh:
        gh = get_github_api()
    wl = []
    all_repos = []
    plone = gh.get_organization('plone')
    for repo in plone.get_repos():
        repo_name = repo.name
        for white_re in white_list_re:
            if re.match(white_re, repo_name):
                wl.append(repo_name)
        all_repos.append(repo_name)
    # remove duplicates
    wl = list(set(wl))
    for black_re in black_list_re:
        for repo_name in wl:
            if re.match(black_re, repo_name):
                wl.remove(repo_name)
    return wl


if __name__ == "__main__":
    # gh = Github()
    gh = None
    get_github_repo_list(gh)
