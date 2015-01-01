#!/usr/bin/env python

import json
import os
import xml.etree.ElementTree as ET

import requests

DATADIR = "/Users/gback/data/rfc/"
BASE_URL = "http://localhost:9200/"
INDEX = "rfc"

RFCs = {}

def load_metadata():
    print "Loading RFC-index metadata file..."
    metadata_file = os.path.join(DATADIR, 'rfc-index.xml')
    tree = ET.parse(metadata_file)
    root = tree.getroot()
    print "...done"

    count = 0
    # RFCs don't start at the beginning of the file.
    for child in root:
        if not child.tag.endswith("rfc-entry"):
            continue

        rfc = {'authors': []}
        for data in child:
            if data.tag.endswith("doc-id"):
                # Remove leading 0's
                id = data.text[3:].lstrip('0')
                rfc['id'] = id
            if data.tag.endswith("title"):
                rfc['title'] = data.text
            if data.tag.endswith("author"):
                rfc['authors'].append(data[0].text)
        count += 1

        RFCs[id] = rfc

    print "%d RFCs loaded" % count

def main():
    load_metadata()

    r = requests.delete(BASE_URL + INDEX)
    print r.json()

    r = requests.put(BASE_URL + INDEX)
    print r.json()

    # Use all RFCs
    txt_dir = os.path.join(DATADIR, "txt")
    for fn in os.listdir(txt_dir)[:]:
        rfc_num = fn[3:-4]
        full_fn = os.path.join(txt_dir, fn)
        with open(full_fn) as f:
            data = f.read().decode('latin1')

        try:
            payload = RFCs[rfc_num]
        except KeyError:
            print "No metadata for RFC %s" % rfc_num
            continue
        payload['body'] = data

        url = BASE_URL + INDEX + "/external/rfc" + rfc_num
        r = requests.put(url, data=json.dumps(payload))
        print str(r.json())[:500]


if __name__ == '__main__':
    main()
