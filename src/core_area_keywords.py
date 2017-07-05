#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: format_string_scan

:Synopsis:
 
:Author:
    costa

:Created:
    6/15/17
"""

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S%z', filename='format_string_scan' + '.log',
                    level=logging.INFO)

logger = logging.getLogger('core_area_keywords')

import requests
from lxml import etree
import sys


def scan_format_string(black_list=None):
    results_dict = {}
    format_strings = {}
    base_url = 'https://pasta.lternet.edu/package/eml'
    xpath = '//keywordSet/keyword'
    core_areas = ['Disturbance Patterns', 'Inorganic Nutrients', 'Organic Matter', 'Populations', 'Primary Production']
    scopes = requests.get(url=base_url).text.split('\n')
    for scope in scopes:
        if scope not in black_list and scope.startswith('knb-lter') :
            scope_dict = {}
            for core_area in core_areas:
                scope_dict[core_area] = 0
            identifiers = requests.get(url=base_url + '/' + scope).text.split('\n')
            for identifier in identifiers:
                package_id = scope + '.' + identifier
                #print('{package_id}'.format(package_id=package_id))
                try:
                    url = 'http://pasta.lternet.edu/package/metadata/eml/' + scope + '/' + identifier + '/newest'
                    tree = etree.parse(url)
                    path = tree.findall(xpath)
                    if path:
                        for elmt in path:
                            keyword = elmt.text.strip()
                            for core_area in core_areas:
                                if core_area.lower() == keyword.lower():
                                    scope_dict[core_area] += 1
                except Exception as e:
                    logger.error(e)
            results_dict[scope] = scope_dict
    print('#site,{ca0},{ca1},{ca2},{ca3},{ca4}'.format(ca0=core_areas[0],
                                                       ca1=core_areas[1],
                                                       ca2=core_areas[2],
                                                       ca3=core_areas[3],
                                                       ca4=core_areas[4]))
    for scope, scope_dict in results_dict.items():
        site_abbrev = scope[9:].upper()
        row = site_abbrev + ',' + str(scope_dict[core_areas[0]]) + ',' + str(scope_dict[core_areas[1]]) + ',' + str(scope_dict[core_areas[2]]) + ',' + str(scope_dict[core_areas[3]]) + ',' + str(scope_dict[core_areas[4]])
        print(row)


def main():

    black_list = ('lter-landsat', 'lter-landsat-ledaps', 'ecotrends', 'knb-lter-nin', 'knb-lter-nwk')
    scan_format_string(black_list=black_list)

    return 0


if __name__ == "__main__":
    main()
