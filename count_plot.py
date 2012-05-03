#!/usr/bin/env python3

import sys, datetime
import saccharina
from pprint import pprint

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: %s <api_key> <zone> <query>" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    api_key, zone = [t.strip() for t in sys.argv[1:3]]
    queries = [t.strip() for t in sys.argv[3:]]
    t = saccharina.instance(api_key, saccharina.FileCache('./cache'))

    def month_iter(start_date, end_date):
        year, month = None, None
        date = start_date
        one_day = datetime.timedelta(days=1)
        while date < end_date:
            if date.year != year or date.month != month:
                year, month = date.year, date.month
                yield year, month
            date += one_day

    def histo_iter():
        for year, month in month_iter(datetime.date(1870, 1, 1), datetime.date(1957, 1, 1)):
            def mk(query):
                q = 'date:[%d TO %d]' % (year, year)
                if query is not None:
                    q += " " + query
                searcher = t.searcher(zone, q)
                searcher['facet'] = 'year'
                searcher['l-decade'] = '%d' % (year/10)
                searcher['l-year'] = '%d' % (year)
                searcher['l-month'] = '%.2d' % (month)
                return searcher
            def get_total(query):
                page = mk(query)[0]
                return [zone for zone in page][0].total
            yield [year, month, get_total(None)] + [get_total(t) for t in queries]

    import csv
    writer = csv.writer(sys.stdout)
    writer.writerow(["year", "month", "total"] + queries)
    for row in histo_iter():
        writer.writerow(row)
