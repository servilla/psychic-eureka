#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: thesauri_scan

:Synopsis:
 
:Author:
    servilla

:Created:
    6/16/17
"""

import logging
import xml.etree.ElementTree as ET

import requests

import sites

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    #filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('thesauri_scan')


def flatten(string=None):
    s = string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    tokens = s.split(' ')
    word = ''
    for token in tokens:
        if len(token):
            word += token + ' '
    return word.strip()


def main():

    thesauri_dict = {}

    base_url = 'https://pasta.lternet.edu/package'
    scopes = requests.get(url=base_url + '/eml').text.split('\n')
    for scope in scopes:
        if scope in sites.LTER:
            identifiers = requests.get(url=base_url + '/eml/' + scope).text.split('\n')
            for identifier in identifiers:
                revision = requests.get(url=base_url + '/eml/' + scope + '/' +
                                identifier + '?filter=newest').text.split('\n')
                pid = scope + '.' + identifier + '.' + revision[0]
                print('Poking: {}'.format(pid))
                metadata_url = base_url + '/metadata/eml/' + scope + '/' + \
                               identifier + '/' + revision[0]
                eml = requests.get(url=metadata_url)
                if eml.status_code == requests.codes.ok:
                    eml_xml = eml.text
                    eml_tree = ET.ElementTree(ET.fromstring(eml_xml.strip()))
                    for keywordSet in eml_tree.iter('keywordSet'):
                        thesauri = keywordSet.findall('./keywordThesaurus')
                        for thesaurus in thesauri:
                            if thesaurus.text is not None:
                                t = flatten(thesaurus.text.strip())
                                print('    {}'.format(t))
                                if thesaurus.text in thesauri_dict:
                                    thesauri_dict[t] += 1
                                else:
                                    thesauri_dict[t] = 1

    with open('thesauri.txt', mode='w') as f:
        for thesaurus in thesauri_dict:
            print('{}: {}'.format(thesaurus, thesauri_dict[thesaurus]))
            print('{}: {}'.format(thesaurus, thesauri_dict[thesaurus]), file=f)


    return 0


if __name__ == "__main__":
    main()