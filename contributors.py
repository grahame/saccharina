#!/usr/bin/env python3

import sys
import saccharina
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s <api_key> [.. contributors ..]" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    api_key = sys.argv[1].strip()
    contributors = sys.argv[2:]
    t = saccharina.instance(api_key)
    if len(contributors) == 0:
        contribs = t.contributors()
        for contrib, attrs in contribs():
            pprint(attrs)
    else:
        for contributor_id in contributors:
            contrib = t.contributor(contributor_id)
            contrib['reclevel'] = 'full'
            pprint(contrib())
