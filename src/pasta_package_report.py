#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: pasta_package_report

:Synopsis:
    Lists data package title, DOI, and identifier for data packages in PASTA

:Author:
    servilla

:Created:
    7/12/17
"""

import logging
import os
import sys

from docopt import docopt
import requests
import xml.etree.ElementTree as ET

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z',
                    # filename='$NAME' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('pasta_package_report')

BASE_URL = 'https://pasta.lternet.edu'


def flatten(string=None):
    s = string.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    tokens = s.split(' ')
    word = ''
    for token in tokens:
        if len(token):
            word += token + ' '
    return word.strip()


def get_doi(base_url=None, path=None):
    url = base_url + '/package/doi/eml/' + path
    try:
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            logger.error(
                'Bad status code ({code}) for {url}'.format(
                    code=r.status_code, url=url))
            sys.exit(1)
        else:
            return r.text.strip()
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def get_eml_metadata(base_url=None, path=None):
    url = base_url + '/package/metadata/eml/' + path
    try:
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            logger.error(
                'Bad status code ({code}) for {url}'.format(
                    code=r.status_code, url=url))
            sys.exit(1)
        else:
            return r.text.strip()
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def get_identifiers(base_url=None, scope=None):
    try:
        url = base_url + '/package/eml/' + scope
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            logger.error('Bad status code ({code}) for {url}'.format(
                code=r.status_code, url=url))
            sys.exit(1)
        else:
            return [_.strip() for _ in (r.text).split(os.linesep)]
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def get_newest_revision(base_url=None, scope=None, identifier=None):
    url = base_url + '/package/eml/' + scope + '/' + identifier \
          + '?filter=newest'
    try:
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            logger.error(
                'Bad status code ({code}) for {url}'.format(
                    code=r.status_code, url=url))
            sys.exit(1)
        else:
            return r.text.strip()
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def get_scopes(base_url=None):
    try:
        url = base_url + '/package/eml'
        r = requests.get(url)
        if r.status_code != requests.codes.ok:
            logger.error('Bad status code ({code}) for {url}'.format(
                code=r.status_code, url=url))
            sys.exit(1)
        else:
            return [_.strip() for _ in (r.text).split(os.linesep)]
    except Exception as e:
        logger.error(e)
        sys.exit(1)


def get_title(eml_xml=None):
    eml = ET.fromstring(eml_xml)
    title = eml.find('./dataset/title')
    return flatten(title.text)


def main(argv):
    """
    Prints PASTA data package information for newest revision: identifier, DOI,
    and title

    Usage:
        pasta_package_report.py [-s | --scope <scope>]  [-o | --output <output>]
        pasta_package_report.py -h | --help

    Options:
        -s --scope    Restrict to given scope
        -o --output   Output results to file
        -h --help     This page

    """
    args = docopt(str(main.__doc__))

    scope = args['<scope>']
    output = args['<output>']

    if output is None:
        fp = sys.stdout
    else:
        fp = open(output, 'w')

    document_id = {}

    if scope is None:
        scopes = get_scopes(base_url=BASE_URL)
    else:
        scopes = [scope]

    # Build dict of package identifiers
    for scope in scopes:
        identifiers = get_identifiers(base_url=BASE_URL, scope=scope)
        for identifier in identifiers:
            revision = get_newest_revision(base_url=BASE_URL, scope=scope,
                                           identifier=identifier)
            id = scope + '.' + identifier + '.' + revision
            document_id[id] = {'path': id.replace('.', '/')}

    # Populate report for each package identifier
    for id in document_id:
        path = document_id[id]['path']
        eml = get_eml_metadata(base_url=BASE_URL, path=path)
        document_id[id]['title'] = get_title(eml_xml=eml)
        document_id[id]['doi'] = get_doi(base_url=BASE_URL, path=path)

    print('PACKAGE_ID,TITLE,DOI', file=fp)
    for id in document_id:
        title = document_id[id]['title']
        doi = document_id[id]['doi']
        print('{pid},"{title}",{doi}'.format(pid=id, title=title, doi=doi),
              file=fp)

    return 0


if __name__ == "__main__":
    main(sys.argv)
