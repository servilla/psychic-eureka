#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: offline_scan

:Synopsis:
 
:Author:
    servilla

:Created:
    1/28/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='offline_scan' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('offline_scan')

import requests
from lxml import etree
import sys


def scan_for_offline(black_list=None):

    base_url = 'https://pasta.lternet.edu/package/eml'
    scopes = requests.get(url=base_url).text.split('\n')
    for scope in scopes:
        if scope not in black_list:
            identifers = requests.get(url=base_url + '/' + scope).text.split('\n')
            for identifier in identifers:
                revision = requests.get(url=base_url + '/' + scope + '/' +
                                identifier).text.split('\n')
                pid = scope + '.' + identifier + '.' + revision[0]
                try:
                    tree = etree.parse(
                        'http://pasta.lternet.edu/package/metadata/eml/' + scope
                        + '/' + identifier + '/' + revision[0])
                    if tree.find('//offline'):
                        print('{pid}, 1'.format(pid=pid))
                    sys.stdout.flush()
                except Exception as e:
                    logger.error(e)


def main():

    black_list = ('lter-landsat', 'lter-landsat-ledaps', 'ecotrends')
    scan_for_offline(black_list=black_list)

    return 0


if __name__ == "__main__":
    main()
