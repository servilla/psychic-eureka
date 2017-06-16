#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: keyword_scan

:Synopsis:
 
:Author:
    servilla

:Created:
    6/15/17
"""

import logging
import xml.etree.ElementTree as ET

import requests

import sites

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    #filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('keyword_scan')


def main():

    keys = ['organic matter', 'inorganic nutrients', 'populations',
            'disturbance patterns', 'primary production']
    scope_dict = {
        'knb-lter-and': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-arc': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-bes': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-bnz': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-cap': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-cce': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-cdr': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-cwt': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-fce': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-gce': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-hbr': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-hfr': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-jrn': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-kbs': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-knz': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-luq': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-mcm': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-mcr': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-nin': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-ntl': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-nwk': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-nwt': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-pal': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-pie': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-sbc': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-sev': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-sgs': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
        'knb-lter-vcr': {'organic matter': 0, 'inorganic nutrients': 0,
                         'populations': 0, 'disturbance patterns': 0,
                         'primary production': 0},
    }

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
                        keywords = keywordSet.findall('./keyword')
                        for keyword in keywords:
                            if keyword.text is not None:
                                word = keyword.text.lower()
                                print('    {}'.format(word))
                                if word in keys:
                                    scope_dict[scope][word] += 1

    with open('core_areas.txt', mode='w') as f:
        for scope in scope_dict:
            print('{}: {}'.format(scope, scope_dict[scope]))
            print('{}: {}'.format(scope, scope_dict[scope]), file=f)


    return 0


if __name__ == "__main__":
    main()