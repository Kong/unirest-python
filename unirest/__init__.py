'''
The MIT License

Copyright (c) 2013 Mashape (http://mashape.com)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import urllib
import base64
import threading
import gzip
from StringIO import StringIO
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import threading

try: 
	import json
except ImportError: 
	import simplejson as json

USER_AGENT = "unirest-python/1.1.5"

_defaultheaders = {}
_timeout = 10

_httplib = None
try:
    from google.appengine.api import urlfetch
    _httplib = 'urlfetch'
except ImportError:
    pass

if not _httplib:
    import urllib2
    _httplib = "urllib2"

# Register the streaming http handlers
register_openers()

def __request(method, url, params = {}, headers ={}, auth = None, callback = None):
    # Lowercase header keys
    headers = dict((k.lower(), v) for k, v in headers.iteritems())
    headers["user-agent"] = USER_AGENT
    
    data, post_headers = __encode(params)
    if post_headers is not None:
        headers = dict(headers.items() + post_headers.items())

    headers['Accept-encoding'] = 'gzip'

    if auth is not None:
        if len(auth) == 2:
            user = auth[0]
            password = auth[1]
            headers['Authorization'] = "Basic " + base64.b64encode(user + ":" + password)

    headers = dict(headers.items() + _defaultheaders.items())

    _unirestResponse = None
    if _httplib == "urlfetch":
        res = urlfetch.fetch(url, payload=data, headers=headers, method=method)
        _unirestResponse = UnirestResponse(res.status_code, response.headers, response.content)
    else:
        req = urllib2.Request(url, data, headers)
        req.get_method = lambda: method
        try:
            response = urllib2.urlopen(req, timeout=_timeout)
        except urllib2.HTTPError, e:
            response = e

        _unirestResponse = UnirestResponse(response.code, response.headers, response.read())
        
    if callback is None or callback == {}:
        return _unirestResponse
    else:
        callback(_unirestResponse)

# The following methods in the Mashape class are based on Stripe's python bindings
# which are under the MIT license. See https://github.com/stripe/stripe-python
def __encode_dict(stk, key, dictvalue):
    n = {}
    for k, v in dictvalue.iteritems():
        k = __utf8(k)
        if type(v) is not file:
            v = __utf8(v)
            n["%s[%s]" % (key, k)] = v
    stk.extend(__encode_inner(n))

def __encode_inner(d):
    """
    We want post vars of form:
    {'foo': 'bar', 'nested': {'a': 'b', 'c': 'd'}}
    to become:
    foo=bar&nested[a]=b&nested[c]=d
    """
    # special case value encoding
    ENCODERS = {
        dict: __encode_dict
    }

    stk = []
    for key, value in d.iteritems():
        key = __utf8(key)
        try:
            encoder = ENCODERS[value.__class__]
            encoder(stk, key, value)
        except KeyError:
            # don't need special encoding
            value = __utf8(value)
            stk.append((key, value))
    return stk

def __utf8(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value

def __encode(d):
    """
    Internal: encode a string for url representation
    """
    if type(d) is dict:
        for key, value in d.iteritems():
            if type(value) is file:
                # It it contains a file it's multipart/data
                return multipart_encode(d);
    
        # Otherwise just regularly encode it
        return urllib.urlencode(__encode_inner(d)), None
    else:
        return d, None

# End of Stripe methods.

HEADERS_KEY = "headers";
CALLBACK_KEY = "callback";
PARAMS_KEY = "params";
AUTH_KEY = "auth";

def get_parameters(kwargs):
    params = kwargs.get(PARAMS_KEY, {})
    if params is not None and type(params) is dict:
        return dict((k, v) for k, v in params.iteritems() if v is not None)
    return params

def get(url, **kwargs):
    params = get_parameters(kwargs)
    if len(params) > 0:
        if url.find("?") == -1:
            url += "?"
        else:
            url += "&"
        url += urllib.urlencode(__encode_inner(dict((k, v) for k, v in params.iteritems() if v is not None))) # Removing None values/encode unicode objects

    return __dorequest("GET", url, {}, kwargs.get(HEADERS_KEY, {}), kwargs.get(AUTH_KEY, None), kwargs.get(CALLBACK_KEY, None))
    
def post(url, **kwargs):
    return __dorequest("POST", url, get_parameters(kwargs), kwargs.get(HEADERS_KEY, {}), kwargs.get(AUTH_KEY, None), kwargs.get(CALLBACK_KEY, None))
    
def put(url, **kwargs):
    return __dorequest("PUT", url, get_parameters(kwargs), kwargs.get(HEADERS_KEY, {}), kwargs.get(AUTH_KEY, None), kwargs.get(CALLBACK_KEY, None))
    
def delete(url, **kwargs):
    return __dorequest("DELETE", url, get_parameters(kwargs), kwargs.get(HEADERS_KEY, {}), kwargs.get(AUTH_KEY, None), kwargs.get(CALLBACK_KEY, None))
    
def patch(url, **kwargs):
    return __dorequest("PATCH", url, get_parameters(kwargs), kwargs.get(HEADERS_KEY, {}), kwargs.get(AUTH_KEY, None), kwargs.get(CALLBACK_KEY, None))

def default_header(name, value):
    _defaultheaders[name] = value

def clear_default_headers():
    _defaultheaders.clear()
    
def timeout(seconds):
    global _timeout
    _timeout = seconds

def __dorequest(method, url, params, headers, auth, callback = None):
    if callback is None:
        return __request(method, url, params, headers, auth)
    else:
        thread = threading.Thread(target=__request, args=(method, url, params, headers, auth, callback))
        thread.start()
        return thread

class UnirestResponse(object):
    def __init__(self, code, headers, body):
        self._code = code
        self._headers = headers
        
        if headers.get("Content-Encoding") == 'gzip':
            buf = StringIO(body)
            f = gzip.GzipFile(fileobj=buf)
            body = f.read()

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
