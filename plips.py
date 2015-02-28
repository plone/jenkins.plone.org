# -*- coding: utf-8 -*-
"""Add all existing PLIPs to jobs.yml

Scan buildout.coredev active branches for PLIPs cfg files and add them to
the list of jobs to be created by jenkins-job-builder.
"""
import os
import re
import subprocess


GIT_FOLDER = 'tmp'
GIT_URL = 'https://github.com/plone/buildout.coredev.git'
BRANCHES = (
    '4.3',
    '5.0',
)


def get_plips():
    """Find all PLIPs cfg files on buildout.coredev branches."""
    regex = re.compile(r'plip(\d+)-*(.+).cfg')
    plips = []

    for branch in BRANCHES:
        p = subprocess.Popen(
            ['git', 'checkout', branch, ],
            cwd=GIT_FOLDER
        )
        p.wait()

        for plip in sorted(os.listdir('{0}/plips'.format(GIT_FOLDER))):
            data = regex.match(plip)
            if data:
                plip_number = data.groups()[0]
                plip_name = data.groups()[1]
                plips.append(
                    {'branch': branch,
                     'number': plip_number,
                     'name': plip_name,
                     'cfg': 'plips/{0}'.format(plip),
                     }
                )
    return plips


def update_jobs_yml(plips):
    """Read jjb jobs definition and update PLIPs project."""
    jobs_file = 'jobs.yml'
    new_jobs_file = 'jobs-tmp.yml'

    with open(jobs_file) as jobs_file_handler, \
            open(new_jobs_file, 'w') as new_jobs_file_handler:

        found = False
        for line in jobs_file_handler.readlines():
            # look for the marker PLIPs project and override
            if not found and line.strip() == 'name: PLIPs':
                found = True

                new_jobs_file_handler.write(line)
                new_jobs_file_handler.write('    plip:\n')
                for plip in plips:
                    write_job_definition(plip, new_jobs_file_handler)

            elif not found:
                new_jobs_file_handler.write(line)

            # once all previously defined plips are processed,
            # write the ending jobs and template and let it copy verbatim again
            if found and line.strip() == "- 'plip-{plip}'":
                new_jobs_file_handler.write('\n    jobs:\n')
                new_jobs_file_handler.write(line)
                found = False

    os.rename(new_jobs_file, jobs_file)


def write_job_definition(plip, file_handler):
    """Write jjb definition for the given plip on the given file."""
    job_id = '{0}-{1}-{2}'.format(
        plip['branch'],
        plip['number'],
        plip['name'],
    )
    file_handler.write('        - {0}:\n'.format(job_id))
    file_handler.write('            buildout: {0}\n'.format(plip['cfg']))
    file_handler.write('            branch: {0}\n'.format(plip['branch']))


def main():
    # remove and download again buildout.coredev
    subprocess.call(['rm', '-rf', GIT_FOLDER ])
    subprocess.call(['git', 'clone', '-q', GIT_URL, GIT_FOLDER])

    plips = get_plips()
    update_jobs_yml(plips)


if __name__ == '__main__':
    main()
