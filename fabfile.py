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


def push():
    """Creates github post-commit hooks to trigger the Jenkins jobs for
    buildout.coredev.
    """
    for plone_version in plone_versions:
        print("")
        print("Plone %s" % plone_version)
        print("---------")
        sources_cfg_url = 'https://raw.github.com/plone/buildout.coredev/' + \
            '%s/sources.cfg' \
            % plone_version
        sources_cfg = urllib2.urlopen(sources_cfg_url)
        print("Read package list from %s" % sources_cfg_url)
        html = sources_cfg.read()
        with requests.session(auth=(github_username, github_password)) as s:
            for line in html.split("\n"):
                if "${remotes:plone}" in line:
                    package = line.split("${remotes:plone}")[1]\
                        .split("pushurl")[0]\
                        .strip(" ").strip("/")
                    #repo_url = "git://github.com/plone/%s" % package
                    existing_hooks = json.loads(
                        s.get(GH_URL + '/repos/plone/%s/hooks' % \
                            package.strip(".git")).content)
                    if not 'message' in existing_hooks:
                        jenkins_hooks = [x for x in existing_hooks \
                            if x['name'] == u'web' and \
                               'jenkins.plone.org/job/plone-%s' % \
                               plone_version in x['config']['url']]
                        for jenkins_hook in jenkins_hooks:
                            #print("Delete post-commit hook for %s" % \
                            #    package.strip(".git"))
                            s.delete(GH_URL + '/repos/plone/%s/hooks/%s' % \
                                (package.strip(".git"), jenkins_hook['id']))
                        # Create a new hook
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
