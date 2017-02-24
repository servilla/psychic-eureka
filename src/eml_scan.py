#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: eml_scan

:Synopsis:
 
:Author:
    servilla

:Created:
    1/28/17
"""

from __future__ import print_function

import logging

"""
logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='eml_scan' + '.log',
                    level=logging.INFO)
"""
logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.INFO)

logger = logging.getLogger('eml_scan')

import requests
from lxml import etree
import sys
import getopt


def do_scan(environment, sites, filter, outfile, xpath, quiet):
    packages = 0
    packages_with_element = 0
    total_cnt = 0
    base_url = environment + '/package/'
    url = base_url + 'eml/'
    scopes = requests.get(url=url).text.split('\n')
    if sites is None:
        sites = scopes
    for scope in scopes:
        if scope in sites:
            url = base_url +  'eml/' + scope
            identifiers = requests.get(url=url).text.split('\n')
            for identifier in identifiers:
                url = base_url + 'eml/' + scope + '/' + identifier + filter
                revision = requests.get(url=url).text.split('\n')
                pid = scope + '.' + identifier + '.' + revision[0]
                try:
                    url = base_url + 'metadata/eml/' + scope + '/' \
                          + identifier + '/' + revision[0]
                    tree = etree.parse(url)
                    path = tree.findall(xpath)
                    packages += 1
                    cnt = 0
                    if path:
                        packages_with_element += 1
                        cnt = len(path)
                    if not quiet:
                        print('{pid}: xpath={xpath} count={cnt}'.format(
                                pid=pid, xpath=xpath, cnt=cnt, file=outfile))
                        sys.stdout.flush()
                    total_cnt += cnt
                except Exception as e:
                    logger.error(e)
    print('Packages analyzed: {packages}'.format(packages=packages))
    print('Packages with xpath \"{xpath}\": {packages_with_element}'.format(
        xpath=xpath, packages_with_element=packages_with_element))
    print('Number of xpath \"{xpath}\" elements: {total_cnt}'.format(
        xpath=xpath, total_cnt=total_cnt))


def site_list(str_list=None):

    list = str_list.split(',')
    for i in range(len(list)):
        list[i] = list[i].strip()

    return list


def main(argv):

    from sites import LTER
    from sites import EDI

    synopsis = 'List PASTA data packages in document identifier format that ' \
               'contain the specific xpath, including occurrences.'

    usage = 'Usage: python2 ./eml_scan.py -h (help) | [-e PASTA ' \
            'environment (\"pasta\" | \"pasta-s\" | \"pasta-d\")] ' \
            '[-s sites (e.g., \"knb-lter-nin,knb-lter-sbc\")] ' \
            '[-L LTER only] ' \
            '[-E EDI only] ' \
            '[-n newest only] ' \
            '[-q quiet]' \
            '[-o output file] ' \
            '<xpath>'

    if len(argv) == 0:
        logger.error(usage)
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, 'LEhnqe:s:o:')
    except getopt.GetoptError as e:
        logger.error('Unrecognized command line flag: {0}'.format(e))
        logger.error(usage)
        sys.exit(1)

    _sites = None
    _filter = ''
    _env = 'http://pasta.lternet.edu'
    _out = sys.stdout
    _quiet = False

    for opt, arg in opts:
        if opt == '-h':
            print(synopsis)
            print(usage)
            sys.exit(0)
        elif opt == '-L':
            if not _sites:
                _sites = LTER
        elif opt == '-E':
            if not _sites:
                _sites = EDI
        elif opt == '-n':
            _filter = '?filter=newest'
        elif opt == '-q':
            _quiet = True
        elif opt == '-e':
            if arg not in ('pasta', 'pasta-s', 'pasta-d'):
                logger.error('Environment \"{arg}\" not recognized!'.format(
                    arg=arg))
                logger.error(usage)
                sys.exit(1)
            _env = 'http://' + arg + '.lternet.edu'
        elif opt == '-o':
            _out = open(arg, 'w')
        elif opt == '-s':
            if not _sites:
                _sites = site_list(arg)
        else:
            logger.error(usage)
            sys.exit(1)

    xpath = args[0]

    do_scan(environment=_env, sites=_sites, filter=_filter,
            outfile=_out, xpath=xpath, quiet=_quiet)

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])