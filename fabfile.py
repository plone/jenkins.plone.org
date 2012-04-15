#!bin/zopepy
import json
import requests
import urllib2
from auth import github_username
from auth import github_password
from auth import jenkins_username
from auth import jenkins_password

hook_url = 'https://%s:%s@jenkins.plone.org/job/plone-4.2/build' % (
    jenkins_username,
    jenkins_password
    )

GH_URL = 'https://api.github.com'

sources = urllib2.urlopen(
    'https://raw.github.com/plone/buildout.coredev/4.2/sources.cfg')
html = sources.read()


def push():
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
                    if not any(h['name'] == 'web' and \
                        h['config']['url'] == hook_url \
                        for h in existing_hooks):
                        # Create a new hook
                        print("Push %s" % package)
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
                    else:
                        # Edit/update a hook
                        print("Update %s" % package)
                        hook = [
                            x for x in existing_hooks \
                            if 'config' in x and \
                            'url' in x['config'] and \
                            x['config']['url'] == hook_url]
                        if len(hook) > 0:
                            hook_id = hook[0]['id']
                            req = {
                                'name': 'web',
                                'active': True,
                                'config': {
                                    'url': hook_url,
                                    'insecure_ssl': 1,
                                }
                            }
                            hook_id = 1
                            s.post(GH_URL + '/repos/plone/%s/hooks%s' % \
                                (package.strip(".git"), hook_id),
                                data=json.dumps(req))
                        else:
                            print("Ignore %s" % package)
