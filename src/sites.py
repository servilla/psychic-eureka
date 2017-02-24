#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: sites

:Synopsis:
 
:Author:
    servilla

:Created:
    2/23/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.INFO)

logger = logging.getLogger('sites')


LTER = (
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

EDI = (
    'edi',
)


def main():
    return 0


if __name__ == "__main__":
    main()