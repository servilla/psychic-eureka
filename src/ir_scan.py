#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: ir_scan

:Synopsis:
 
:Author:
    servilla

:Created:
    1/28/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='ir_scan' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('ir_scan')

import requests
from lxml import etree
import sys


def get_newest_pids():
    sites = (
        'knb-lter-and',
        'knb-lter-arc',
        'knb-lter-bes',
        'knb-lter-bnz',
        'knb-lter-cap',
        'knb-lter-cce',
        'knb-lter-cdr',
        'knb-lter-cwt',
        'knb-lter-fce',
        'knb-lter-gce',
        'knb-lter-hbr',
        'knb-lter-hfr',
        'knb-lter-jrn',
        'knb-lter-kbs',
        'knb-lter-knz',
        'knb-lter-luq',
        'knb-lter-mcm',
        'knb-lter-mcr',
        'knb-lter-nin',
        'knb-lter-ntl',
        'knb-lter-nwk',
        'knb-lter-nwt',
        'knb-lter-pal',
        'knb-lter-pie',
        'knb-lter-sbc',
        'knb-lter-sev',
        'knb-lter-sgs',
        'knb-lter-vcr',
    )
    base_url = 'https://pasta.lternet.edu/package/eml'
    scopes = requests.get(url=base_url).text.split('\n')
    for scope in scopes:
        if scope in sites:
            identifers = requests.get(url=base_url + '/' + scope).text.split('\n')
            for identifier in identifers:
                revision = requests.get(url=base_url + '/' + scope + '/' +
                                identifier + '?filter=newest').text.split('\n')
                pid = scope + '.' + identifier + '.' + revision[0]
                try:
                    tree = etree.parse(
                        'http://pasta.lternet.edu/package/metadata/eml/' + scope
                        + '/' + identifier + '/' + revision[0])
                    if tree.find('//intellectualRights'):
                        print('{pid}, 1'.format(pid=pid))
                    else:
                        print('{pid}, 0'.format(pid=pid))
                    sys.stdout.flush()
                except Exception as e:
                    logger.error(e)


def main():

    get_newest_pids()

    return 0


if __name__ == "__main__":
    main()