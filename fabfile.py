#!bin/zopepy
import sys
import json
import requests
import urllib2
from auth import github_username
from auth import github_password
from auth import jenkins_username
from auth import jenkins_password

GH_URL = 'https://api.github.com'
JENKINS_URL = 'jenkins.plone.org'

plone_versions = ['4.2', '4.3']


def _get_sources(sources_cfg_url):
    """Get a list of all packages for a certain Plone version from the
       buildout.coredev sources.cfg.
    """
    print("Read package list from %s" % sources_cfg_url)
    sources_cfg = urllib2.urlopen(sources_cfg_url)
    html = sources_cfg.read()
    packages = []
    for line in html.split("\n"):
        if "${remotes:plone}" in line:
            packages.append(
                line.split("${remotes:plone}/")[1].split(".git")[0])
        if "${remotes:collective}" in line:
            packages.append(
                line.split("${remotes:collective}/")[1].split(".git")[0])
    print("%s packages found." % len(packages))
    return packages


def _delete_existing_hooks(s, package, jenkins_job_name):
    """Delete existing post commit hooks from a package. We make sure that
       hooks for a specific plone version are removed and all other hooks
       remain untouched.
    """
    package_hooks = json.loads(
        s.get(
            GH_URL + '/repos/plone/%s/hooks' %
            package).content)
    if not 'message' in package_hooks:
        coredev_hooks = [
            x for x in package_hooks
            if x['name'] == u'web' and
            '%s/job/%s' % (
                JENKINS_URL,
                jenkins_job_name) in x['config']['url']]
        for coredev_hook in coredev_hooks:
            url = GH_URL + '/repos/plone/%s/hooks/%s' % (
                package,
                coredev_hook['id'])
            response = s.delete(url)
            if response.status_code != 204:
                _failed(url)


def _create_hook(s, package, jenkins_job_name, github_project_name="plone"):
    """Create a post commit hook on github for a certain package that triggers
       the Jenkins job of a specific Plone version.
    """
    print("")
    sys.stdout.write("Create post-commit hook for %s" % package)
    hook_url = 'https://%s:%s@%s/job/%s/build' % (
        jenkins_username,
        jenkins_password,
        JENKINS_URL,
        jenkins_job_name,
    )
    req = {
        'name': 'web',
        'active': True,
        'config': {
            'url': hook_url,
            'insecure_ssl': 1,
        }
    }
    url = GH_URL + '/repos/%s/%s/hooks' % (
        github_project_name,
        package,
    )
    response = s.post(url, data=json.dumps(req))
    if response.status_code == 201:
        _ok()
    else:
        _failed(url)


def _ok():
    sys.stdout.write(" [ \033[92mOK\033[0m ]")


def _failed(url):
    sys.stdout.write(" [ \033[93mFAILED\033[0m ]")
    print("")
    print(url)


def push():
    """Creates github post-commit hooks to trigger the Jenkins jobs for
       buildout.coredev.
    """
    with requests.session(auth=(github_username, github_password)) as s:
        for plone_version in plone_versions:
            print("")
            print("Plone %s" % plone_version)
            print("---------")
            packages = _get_sources(
                'https://raw.github.com/plone/buildout.coredev/%s/sources.cfg'
                % plone_version
            )
            for package in packages:
                _delete_existing_hooks(s, package, "plone-%s" % plone_version)
                _create_hook(s, package, "plone-%s" % plone_version)
            _create_hook(s, "buildout.coredev", "plone-%s" % plone_version)
            print("")


def push_deco():
    """Creates github post-commit hooks to trigger the Jenkins jobs for
       buildout.deco.
    """
    with requests.session(auth=(github_username, github_password)) as s:
        print("")
        print("Deco")
        print("---------")
        packages = _get_sources(
            'https://raw.github.com/plone/buildout.deco/master/sources.cfg'
        )
        for package in packages:
            _delete_existing_hooks(s, package, "deco")
            _create_hook(s, package, "deco")
        _create_hook(s, "buildout.deco", "deco")
        print("")


def push_templer():
    """Creates github post-commit hooks to trigger the Jenkins jobs for
       buildout.deco.
    """
    with requests.session(auth=(github_username, github_password)) as s:
        print("")
        print("Templer")
        print("---------")
        packages = _get_sources(
            'https://raw.github.com/collective/buildout.templer/' +
            'master/buildout.cfg'
        )
        for package in packages:
            _delete_existing_hooks(s, package, "templer")
            _create_hook(s, package, "deco", github_project_name="collective")
        _create_hook(
            s,
            "buildout.templer",
            "templer",
            github_project_name="collective")
        print("")


def push_plone_app_contenttypes():
    """Creates github post-commit hooks to trigger the Jenkins jobs for
       plone.app.contenttypes.
    """
    with requests.session(auth=(github_username, github_password)) as s:
        print("")
        print("plone.app.contenttypes")
        print("---------")
        packages = [
            'plone.app.contenttypes',
            'plone.app.collection',
        ]
        for package in packages:
            _delete_existing_hooks(s, package, "plone.app.contenttypes")
            _create_hook(s, package, "plone.app.contenttypes")
        print("")
