#!bin/zopepy
import json
import requests
import urllib2
from auth import github_username
from auth import github_password
from auth import jenkins_username
from auth import jenkins_password

GH_URL = 'https://api.github.com'

plone_versions = ['4.2', '4.3']


def _get_sources(plone_version):
    """Get a list of all packages for a certain Plone version from the
       buildout.coredev sources.cfg.
    """
    sources_cfg_url = 'https://raw.github.com/plone/buildout.coredev/' + \
        '%s/sources.cfg' \
        % plone_version
    sources_cfg = urllib2.urlopen(sources_cfg_url)
    print("Read package list from %s" % sources_cfg_url)
    html = sources_cfg.read()
    packages = []
    for line in html.split("\n"):
        if "${remotes:plone}" in line:
            packages.append(
                line.split("${remotes:plone}")[1]\
                    .split("pushurl")[0]\
                    .strip(" ").strip("/"))
    return packages


def _delete_existing_hooks(s, package, plone_version):
    """Delete existing post commit hooks from a package. We make sure that
       hooks for a specific plone version are removed and all other hooks
       remain untouched.
    """
    package_hooks = json.loads(
        s.get(GH_URL + '/repos/plone/%s/hooks' % \
            package.strip(".git")).content)
    if not 'message' in package_hooks:
        coredev_hooks = [x for x in package_hooks \
            if x['name'] == u'web' and \
               'jenkins.plone.org/job/plone-%s' % \
               plone_version in x['config']['url']]
        for coredev_hook in coredev_hooks:
            #print("Delete post-commit hook for %s" % \
            #    package.strip(".git"))
            s.delete(GH_URL + '/repos/plone/%s/hooks/%s' % \
                (package.strip(".git"), coredev_hook['id']))


def _create_hook(s, package, plone_version):
    """Create a post commit hook on github for a certain package that triggers
       the Jenkins job of a specific Plone version.
    """
    print("Create post-commit hook for %s" % \
        package.strip(".git"))
    hook_url = 'https://%s:%s@jenkins.plone.org/job/plone-%s/build' % (
        jenkins_username,
        jenkins_password,
        plone_version,
        )
    req = {
        'name': 'web',
        'active': True,
        'config': {
            'url': hook_url,
            'insecure_ssl': 1,
        }
    }
    s.post(GH_URL + '/repos/plone/%s/hooks' % \
        package.strip(".git"), data=json.dumps(req))


def push():
    """Creates github post-commit hooks to trigger the Jenkins jobs for
       buildout.coredev.
    """
    with requests.session(auth=(github_username, github_password)) as s:
        for plone_version in plone_versions:
            print("")
            print("Plone %s" % plone_version)
            print("---------")
            packages = _get_sources(plone_version)
            for package in packages:
                _delete_existing_hooks(s, package, plone_version)
                _create_hook(s, package, plone_version)
            _create_hook(s, "buildout.coredev", plone_version)
