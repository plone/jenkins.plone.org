# -*- coding: utf-8 -*-
import xml.etree.ElementTree as XML


def custom_history(parser, xml_parent, data):
    """yaml: custom-history

    Show a custom file for the history.
    Requires the Jenkins `Custom History.
    <https://wiki.jenkins-ci.org/display/JENKINS/Custom+History>`_

    :arg str file: filename that will be used to show the history form
    :arg bool exit-on-fail: whether it exit if it fails (default False)

    Example::

      publishers:
        - custom-history:
            file: CHANGES.log
    """
    history_data = XML.SubElement(
        xml_parent,
        'org.jenkinsci.plugins.custom__history.SaveHistory'
    )

    data_property = str(data.get('file'))
    XML.SubElement(history_data, 'fname').text = data_property

    data_property = str(data.get('exit-on-fail', False)).lower()
    XML.SubElement(history_data, 'exitOnFail').text = data_property
