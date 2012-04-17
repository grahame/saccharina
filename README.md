
`saccharina`; named for the Silverfish.

This is a Python 3 binding for the National Library of Australia's
Trove API. See this page for further information about the API:

http://trove.nla.gov.au/general/api

To use this software you'll need to get an API key from the Trove
website.

This software has no affiliation with the National Library of Australia.

See the file `LICENSE` for licensing and copyright information.

There are several example programs included;

Query:

    python3 search.py <api_key> <zone> <query>

for example:

    python3 search.py <api_key> newspaper 'harold holt'

List newspapers:

    newspapers.py <api_key>

Detail on a particular newspaper:

    newspapers.py <api_key> <id>

List contributors:

    contributors.py <api_key>

Detail on a particular contributor:

    contributors.py <api_key> <id>

