#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: datetime_scan

:Synopsis:
 
:Author:
    servilla

:Created:
    5/7/17
"""

import xml.etree.ElementTree as ET
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    # filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('datetime_scan')

import docopt
import requests

import sites


def main():

    dateTime_dict = {}

    base_url = 'https://pasta.lternet.edu/package'
    scopes = requests.get(url=base_url + '/eml').text.split('\n')
    for scope in scopes:
        if scope in sites.EDI:
            identifers = requests.get(url=base_url + '/eml/' + scope).text.split('\n')
            for identifier in identifers:
                revision = requests.get(url=base_url + '/eml/' + scope + '/' +
                                identifier + '?filter=newest').text.split('\n')
                pid = scope + '.' + identifier + '.' + revision[0]
                #print('{}'.format(pid))
                metadata_url = base_url + '/metadata/eml/' + scope + '/' + \
                               identifier + '/' + revision[0]
                eml = requests.get(url=metadata_url)
                if eml.status_code == requests.codes.ok:
                    eml_xml = eml.text
                    eml_tree = ET.ElementTree(ET.fromstring(eml_xml.strip()))
                    for dateTime in eml_tree.iter('dateTime'):
                        formatString = dateTime.find('./formatString')
                        #print(formatString.text)
                        if formatString.text in dateTime_dict:
                            dateTime_dict[formatString.text] += 1
                        else:
                            dateTime_dict[formatString.text] = 1

    with open('formatStr.txt', mode='w') as f:
        for formatString, cnt in dateTime_dict.items():
            print('{fmt}, {cnt}'.format(fmt=formatString, cnt=cnt), file=f)

    return 0


if __name__ == "__main__":
    main()