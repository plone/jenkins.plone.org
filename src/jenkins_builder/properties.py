# -*- coding: utf-8 -*-
import xml.etree.ElementTree as XML


def disk_usage(parser, xml_parent, data):
    """yaml: disk-usage

    Configures Jenkins to monitor the disk usage of jobs.
    Requires the Jenkins `Disk Usage Plugin.
    <https://wiki.jenkins-ci.org/display/JENKINS/Disk+Usage+Plugin>`_

    Example::

      properties:
        - disk-usage
    """
    XML.SubElement(xml_parent, 'hudson.plugins.disk__usage.DiskUsageProperty')
