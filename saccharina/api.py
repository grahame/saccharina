
import urllib.request, urllib.parse, json, copy, os, time
from hashlib import sha256
import pickle

class TroveException(Exception):
    pass

class FileCache:
    def __init__(self, cache_dir):
        self._cache_dir = cache_dir
        self._hit = 0
        self._miss = 0

    def _fname(self, key):
        h = sha256()
        h.update(key.encode('utf8'))
        return os.path.join(self._cache_dir, h.hexdigest())

    def get(self, key):
        try:
            with open(self._fname(key), 'rb') as fd:
                _key, s = pickle.load(fd)
                assert(key == _key)
                self._hit += 1
                return s
        except IOError:
            self._miss += 1
            return None

    def set(self, key, s):
        with open(self._fname(key), 'wb') as fd:
            pickle.dump((key, s), fd)

def instance(api_key, cache=None):
    def api_call(uri, values):
        values = copy.deepcopy(values)
        values['key'] = api_key
        values['encoding'] = 'json'
        uri += '?' + urllib.parse.urlencode(values)
        def _make_call():
            req = urllib.request.Request(uri)
            handle = urllib.request.urlopen(req)
            result = handle.read()
            return result.decode('utf8')
        def _wrap_cache():
            if cache:
                result = cache.get(uri)
                if result is not None:
                    return result
            while True:
                try:
                    result = _make_call()
                except urllib.error.HTTPError as e:
                    if e.code == 403:
                        time.sleep(1)
                        continue
                break
            if cache:
                cache.set(uri, result)
            return result
        result = _wrap_cache()
        return json.loads(result)

    class Response:
        def _set(self, d, *args, c=None):
            for k in args:
                v = d.get(k, None)
                if c is not None:
                    v=c(v)
                setattr(self, k, v)

    class Record:
        def __init__(self, uri):
            self._uri = urllib.parse.urljoin('http://api.trove.nla.gov.au/', uri)
            self._values = {}

        def __setitem__(self, k, v):
            self._values[k] = v

        def __call__(self):
            return api_call(self._uri, self._values)

    class RecordResponse(Response):
        def __init__(self, record_type, record):
            self._record = record
            self._set(self._record, 'category', 'title', 'url', 'snippet', 'relevance', 'date', 'id')

        def get(self):
            return self._record

        def get_record(self):
            return Record(self.url)

    class ZoneResponse(Response):
        def __init__(self, zone):
            self._zone = zone
            self._set(self._zone, 'name', 'records')
            self._set(self.records, 'n', 's', 'total', c=int)

        def __repr__(self):
            return "%s(n=%d,s=%d,total=%d)" % (self.name, self.n, self.s, self.total)
        
        def __iter__(self):
            def _iter():
                for k in self.records:
                    if type(self.records[k]) is not list:
                        continue
                    for v in self.records[k]:
                        yield RecordResponse(k, v)
            return _iter()

    class SearchResponse(Response):
        def __init__(self, resp):
            self._resp = resp['response']
            self._set(self._resp, 'query', 'zone')

        def __iter__(self):
            def _iter():
                for zone in self._resp['zone']:
                    yield ZoneResponse(zone)
            return _iter()

    class PagedSearch:
        def __init__(self, values):
            self._n = 20
            self._values = copy.deepcopy(values)

        def __setitem__(self, k, v):
            self._values[k] = v

        def set_pagesize(self, n):
            if n < 0 or n > 100:
                raise ValueError("invalid page size")
            self._n = n

        def __getitem__(self, page):
            "retrive a page, counting from zero"
            values = copy.deepcopy(self._values)
            values['s'] = page * self._n
            values['n'] = str(self._n)
            base_uri = 'http://api.trove.nla.gov.au/result'
            res = api_call(base_uri, values)
            return SearchResponse(res)

    class Contributor:
        def __init__(self, contributor_id):
            self._id = contributor_id
            self._uri = urllib.parse.urljoin('http://api.trove.nla.gov.au/contributor/', self._id)
            self._values = {}

        def __setitem__(self, k, v):
            self._values[k] = v

        def __call__(self):
            return api_call(self._uri, self._values)

    class ContributorsList:
        def __init__(self, _resp):
            self._resp = _resp
            self._contributors = self._resp['response']['contributor']

        def __iter__(self):
            def _iter():
                for attrs in self._contributors:
                    yield Contributor(attrs['id']), attrs
            return _iter()

    class Contributors:
        def __init__(self):
            self._uri = 'http://api.trove.nla.gov.au/contributor'
            self._values = {}

        def __setitem__(self, k, v):
            self._values[k] = v

        def __call__(self):
            return ContributorsList(api_call(self._uri, self._values))

    class NewspaperTitle:
        def __init__(self, paper_id):
            self._id = paper_id
            self._uri = urllib.parse.urljoin('http://api.trove.nla.gov.au/newspaper/title/', self._id)
            self._values = {}

        def __setitem__(self, k, v):
            self._values[k] = v

        def __call__(self):
            return api_call(self._uri, self._values)

    class NewspaperTitlesList:
        def __init__(self, _resp):
            self._resp = _resp
            self._titles = self._resp['response']['records']['newspaper']

        def __iter__(self):
            def _iter():
                for attrs in self._titles:
                    yield NewspaperTitle(attrs['id']), attrs
            return _iter()

    class NewspaperTitles:
        def __init__(self):
            self._uri = 'http://api.trove.nla.gov.au/newspaper/titles'
            self._values = {}

        def __setitem__(self, k, v):
            self._values[k] = v

        def __call__(self):
            return NewspaperTitlesList(api_call(self._uri, self._values))

    class Trove:
        def searcher(self, zone, q):
            values = {}
            values['zone'] = zone
            values['q'] = q
            return PagedSearch(values)
        
        def record(self, uri):
            return Record(uri)
        
        def newspaper_titles(self):
            return NewspaperTitles()
        
        def newspaper_title(self, title_id):
            return NewspaperTitle(title_id)
        
        def contributors(self):
            return Contributors()

        def contributor(self, contributor_id):
            return Contributor(contributor_id)

    return Trove()
