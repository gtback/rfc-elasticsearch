#!/usr/bin/env python

import sys

import requests

BASE_URL = "http://localhost:9200/"
INDEX = "rfc"

def main():
    term = sys.argv[1]
    r = requests.get(BASE_URL + INDEX + "/_search/?q=%s" % term)
    results = r.json()

    res_count = results['hits']['total']
    time = results['took'] / 1000.0
    print "%s results in %s s" % (res_count, time)
    for hit in results['hits']['hits']:
        print "%s - %s (%s)" % (hit['_id'].upper(), hit['_source']['title'],
                                hit['_score'])


if __name__ == '__main__':
    main()
