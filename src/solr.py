#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':Mod: solr

:Synopsis:
 
:Author:
    servilla

:Created:
    4/11/17
'''

import xml.etree.ElementTree as ET

import requests


def get_tokens(token_str=None):
    """
        Returns a list of tokens as strings from a string of comma separated
        tokens
        
    :param token_str: str of comma separated tokens
    :return: list of tokens
    """
    token_list = []
    if token_str is not None:
        tokens = token_str.split(',')
        for token in tokens:
            token_list.append(token.strip())
    return token_list


def get_count(result_str=None):
    root = ET.fromstring(result_str)
    return int(root.attrib['numFound'])



def do_solr(url=None, query='*', scope='*', fields='*', start=0, rows=10):

    if url is None:
        url = 'https://pasta.lternet.edu/package/search/eml?'

    q = ''
    tokens = get_tokens(query)
    for token in tokens:
        q += '&q=' + token

    s = ''
    tokens = get_tokens(scope)
    for token in tokens:
        s += '&fq=scope:' + token

    f = '&fl='
    tokens = get_tokens(fields)
    for token in tokens:
        f += token + ','


    query_string = 'defType=edismax' \
                   '{query}' \
                   '{scope}' \
                   '{fields}' \
                   '&sort=score,desc&sort=packageid,asc' \
                   '&debug=false' \
                   '&start={start}' \
                   '&rows={rows}' \
                   .format(query=q, scope=s, fields=f, start=start, rows=rows)

    solr_query = url + query_string
    print(solr_query)
    r = requests.get(solr_query)
    if r.status_code == requests.codes.ok:
        return r.text
    else:
        return "An error occurred during the Solr query"


def main():

    scope = 'edi'
    fields = 'packageid, doi'
    start = 0
    rows = 3

    result = do_solr(scope=scope, fields=fields, start=start, rows=rows)
    print(result)
    cnt = get_count(result_str=result)
    start += rows
    while start < cnt:
        result = do_solr(scope=scope, fields=fields, start=start, rows=rows)
        print(result)
        start += rows

    return 0


if __name__ == '__main__':
    main()