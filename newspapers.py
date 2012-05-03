#!/usr/bin/env python3

import sys
import saccharina
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s <api_key> [.. titles ..]" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    api_key = sys.argv[1].strip()
    titles = sys.argv[2:]
    t = saccharina.instance(api_key)
    if len(titles) == 0:
        papers = t.newspaper_titles()
        for title, attrs in papers():
            print("%s : %s : %s" % (attrs['id'], attrs['state'], attrs['title']))
    else:
        for title_id in titles:
            title = t.newspaper_title(title_id)
            title['include'] = 'years'
            pprint(title())


