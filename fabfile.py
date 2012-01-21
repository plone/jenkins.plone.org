#!bin/zopepy
import jenkins
from lxml import etree

from auth import JENKINS_URL
from auth import JENKINS_USERNAME
from auth import JENKINS_PASSWORD

CONFIG = {
    'id': 'plone-4.2',
    'name': 'Plone 4.2',
    'repo': 'git://github.com/plone/buildout.coredev.git',
    'packages': [
        {
            'id': 'plone-4.2-plone.app.layout',
            'name': 'plone.app.layout',
            'repo': 'git://github.com/plone/plone.app.layout.git'
        },
        {
            'id': 'plone-4.2-Products.CMFPlone',
            'name': 'Products.CMFPlone',
            'repo': 'git://github.com/plone/Products.CMFPlone.git'
        }
    ]
}


def connect():
    return jenkins.Jenkins(
        JENKINS_URL, JENKINS_USERNAME, JENKINS_PASSWORD)


def get_jobs():
    j = connect()
    for job in j.get_jobs():
        print job['name']


def deploy():
    j = connect()
    plone_job_id = CONFIG['id']
    plone_job_name = CONFIG['name']
    plone_repo = CONFIG['repo']
    # Plone Job Config
    plone_config = open('config/plone.xml', 'r')
    if j.job_exists(plone_job_id):
        print("Reconfig Job %s" % plone_job_id)
        j.reconfig_job(plone_job_id, plone_config.read())
    else:
        print("Create Job %s" % plone_job_id)
        j.create_job(plone_job_id, plone_config.read())
    # Package Job Config
    for package in CONFIG['packages']:
        tree = etree.parse('config/package.xml')
        tree.find("//scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url").text = package['repo']
        tree.find("//customWorkspace").text = plone_repo
        package_config = etree.tostring(tree)
        if j.job_exists(package['id']):
            print("Reconfig Job %s" % package['id'])
            j.reconfig_job(package['id'], package_config)
        else:
            print("Create Job %s" % package['id'])
            j.create_job(package['id'], package_config)


def build():
    j = connect()
    j.build_job(CONFIG['id'])
