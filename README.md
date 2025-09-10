# PLONE JENKINS/CI

This repository is used to configure <https://jenkins.plone.org>

## Servers configuration

Our servers and nodes are configured with [ansible](http://ansible.com)

## Jobs

Get the repository and python:

```shell
git clone git@github.com:plone/jenkins.plone.org
cd jenkins.plone.org
python3.11 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Test changes locally

Double checking the changes befor deploying them is very helpful,
for that, do the following:

```shell
# with a clean repository, run:
jenkins-jobs --conf jobs/config.ini test jobs/jobs.yml -o old --config-xml
# do the actual changes on jobs/* files
jenkins-jobs --conf jobs/config.ini test jobs/jobs.yml -o new --config-xml
# now compare old and new folders
meld old new
```
