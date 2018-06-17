from requests.auth import HTTPBasicAuth

import os
import requests
import subprocess

output = subprocess.check_output(['jenkins-jobs', '--conf', 'config.ini', 'list'])
if not os.path.isdir('current-jobs'):
    os.makedirs('current-jobs')

for jobname in output.splitlines():
    job = jobname.strip()
    print('Downloading configuration for job {0}'.format(job))
    result = requests.get(
        'https://jenkins.plone.org/job/{0}/config.xml'.format(job),
        auth=HTTPBasicAuth(
            os.environ['JENKINS_USER_ID'],
            os.environ['JENKINS_USER_TOKEN'],
        )
    )
    with open('current-jobs/{}'.format(job), 'w') as result_file:
        result_file.write(result.content)
