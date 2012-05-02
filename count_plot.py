#!/usr/bin/env python3

import sys, datetime
import saccharina
from pprint import pprint

## http://api.trove.nla.gov.au/result?zone=newspaper&q=fulltext%3Aaardvark&facet=year&n=0&encoding=json&key=6pi5hht0d2umqcro&l-decade=180&callback=jQuery16207292051145341247_1334747331720&_=1334747350799
## http://api.trove.nla.gov.au/result?zone=newspaper&facet=year&n=0&encoding=json&key=6pi5hht0d2umqcro&l-decade=181&q=date:[1810%20TO%201819]&callback=jQuery16207292051145341247_1334747331721&_=1334747351001

# zone=newspaper&facet=year&n=0&l-decade=181&q=date:[1810 TO 1819]
# zone=newspaper&q=fulltext:aardvark&facet=year&n=0&l-decade=180

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: %s <api_key> <zone> <query>" % sys.argv[0], file=sys.stderr)
        sys.exit(1)
    api_key, zone, query = [t.strip() for t in sys.argv[1:]]
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
        for year, month in month_iter(datetime.date(1900, 1, 1), datetime.date(1960, 1, 1)):
            searcher = t.searcher(zone, 'date:[%d TO %d]' % (year, year))
            searcher['facet'] = 'year'
            searcher['l-decade'] = '%d' % (year/10)
            searcher['l-year'] = '%d' % (year)
            searcher['l-month'] = '%.2d' % (month)
            total_month = searcher[0]
            print(total_month)
            sys.exit(0)
            searcher = t.searcher(zone, 'date:[%d TO %d] AND fulltext:%s' % (year, year, query))
            searcher['facet'] = 'year'
            searcher['l-decade'] = '%d' % (year/10)
            searcher['l-year'] = '%d' % (year)
            searcher['l-month'] = '%.2d' % (month)
            results_month = searcher[0].total
            yield year, month, results_month, total_month

    for year, month, res, total in histo_iter():
        print(results, total)

    sys.exit(0)

    for zone_response in searcher[0]:
        print(zone_response)
        for response in zone_response:
            pass #pprint(response.get())
    sys.exit(0)
    searcher = t.searcher(zone, 'fulltext:' + query)
    searcher['facet'] = 'year'
    searcher['l-decade'] = '181'
    for zone_response in searcher[0]:
        print(zone_response)


