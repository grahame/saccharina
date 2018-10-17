
`saccharina`; named for the Silverfish.
===============

This is a Python 3 binding for the National Library of Australia's
Trove API. See this page for further information about the API:

http://help.nla.gov.au/trove/building-with-trove/api

To use this software you'll need to get an API key from the Trove
website.

This software has no affiliation with the National Library of Australia.

See the file `LICENSE` for licensing and copyright information.

There are several example programs included;

Query:

    search.py <api_key> <zone> <query>

for example:

    search.py <api_key> newspaper 'harold holt'

List newspapers:

    newspapers.py <api_key>

Detail on a particular newspaper:

    newspapers.py <api_key> <id>

List contributors:

    contributors.py <api_key>

Detail on a particular contributor:

    contributors.py <api_key> <id>

Programming notes
========

First call `saccharina.instance` with an API key. This will return a `Trove` instance.

Each method on the `Trove` instance will return a class that is a pseudo-dictionary 
representing some task you might perform, such as searching the archive. Set items 
on this class instance to add extra form attributes to the request;

    t = saccharina.instance(api_key)
    searcher = t.searcher(zone, q)
    searcher['reclevel'] = "full"

The searcher method returns an iterable class instance which will progressively 
return results. Be careful not to break Trove's API limits when using this.

All the other methods return a callable class. Once you have been returned the 
instance, set whatever items you need on it, and then call it `()` to be returned 
the result of performing the API call.

