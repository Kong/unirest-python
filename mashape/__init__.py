import urllib
import base64
import json

_httplib = None
try:
    from google.appengine.api import urlfetch
    _httplib = 'urlfetch'
except ImportError:
    pass

if not _httplib:
    import urllib2
    _httplib = "urllib2"

def request(method, url, params = {}, headers ={}):
    data = encode(params)
    if _httplib == "urlfetch":
        res = urlfetch.fetch(url, payload=data, headers=headers, method=method)
     #   return json.loads(res.content)
        return res.content
    else:
        req = urllib2.Request(url, data, headers)
        req.get_method = lambda: method
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            response = e

        mashapeResponse = MashapeResponse(response.code, response.headers, response.read())
        return mashapeResponse
        #return json.loads(response_html)

# The following methods in the Mashape class are based on Stripe's python bindings
# which are under the MIT license. See https://github.com/stripe/stripe-python
def encode_dict(stk, key, dictvalue):
    n = {}
    for k, v in dictvalue.iteritems():
        k = _utf8(k)
        v = _utf8(v)
        n["%s[%s]" % (key, k)] = v
    stk.extend(_encode_inner(n))

def _encode_inner(d):
    """
    We want post vars of form:
    {'foo': 'bar', 'nested': {'a': 'b', 'c': 'd'}}
    to become:
    foo=bar&nested[a]=b&nested[c]=d
    """
    # special case value encoding
    ENCODERS = {
        dict: encode_dict
    }

    stk = []
    for key, value in d.iteritems():
        key = _utf8(key)
        try:
            encoder = ENCODERS[value.__class__]
            encoder(stk, key, value)
        except KeyError:
            # don't need special encoding
            value = _utf8(value)
            stk.append((key, value))
    return stk

def _utf8(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value

def encode(d):
    """
    Internal: encode a string for url representation
    """
    return urllib.urlencode(_encode_inner(d))

# End of Stripe methods.

class MashapeResponse(object):
    def __init__(self, code, headers, body):
        self._code = code
        self._headers = headers
        self._raw_body = body
        self._body = self._raw_body;
        try:
            self._body = json.loads(self._raw_body)
        except ValueError:
             #Do nothing
             pass
       
    @property
    def code(self):
        return self._code
        
    @property
    def body(self):
        return self._body
        
    @property
    def raw_body(self):
        return self._raw_body

    @property
    def headers(self):
        return self._headers