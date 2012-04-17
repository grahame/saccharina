#!/usr/bin/env python3

import sys
import saccharina
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: %s <api_key> <zone> <query>" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    api_key, zone, query = [t.strip() for t in sys.argv[1:]]
    t = saccharina.instance(api_key)
    for zone_response in t.searcher(zone, query)[0]:
        for record in zone_response:
            print()
            print(record.date, record.relevance)
            print(record.snippet)
            print(record.url)
            rec = record.get()
            rec['include'] = 'articletext'
            rec['reclevel'] = 'full'
            print(rec())


