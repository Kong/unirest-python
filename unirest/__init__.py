'''
The MIT License

Copyright (c) 2013 Mashape (https://www.mashape.com)

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
import utils

from StringIO import StringIO
from poster.streaminghttp import register_openers

try:
    import json
except ImportError:
    import simplejson as json

USER_AGENT = "unirest-python/1.1.6"

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


def __request(method, url, params={}, headers={}, auth=None, callback=None):

    # Encode URL
    url_parts = url.split("\\?")
    url = url_parts[0].replace(" ", "%20")
    if len(url_parts) == 2:
        url += "?" + url_parts[1]

    # Lowercase header keys
    headers = dict((k.lower(), v) for k, v in headers.iteritems())
    headers["user-agent"] = USER_AGENT

    data, post_headers = utils.urlencode(params)
    if post_headers is not None:
        headers = dict(headers.items() + post_headers.items())

    headers['Accept-encoding'] = 'gzip'

    if auth is not None:
        if len(auth) == 2:
            user = auth[0]
            password = auth[1]
            encoded_string = base64.b64encode(user + ':' + password)
            headers['Authorization'] = "Basic " + encoded_string

    headers = dict(headers.items() + _defaultheaders.items())

    _unirestResponse = None
    if _httplib == "urlfetch":
        res = urlfetch.fetch(url, payload=data, headers=headers, method=method, deadline=_timeout)
        _unirestResponse = UnirestResponse(res.status_code,
                                           res.headers,
                                           res.content)
    else:
        req = urllib2.Request(url, data, headers)
        req.get_method = lambda: method
        try:
            response = urllib2.urlopen(req, timeout=_timeout)
        except urllib2.HTTPError, e:
            response = e

        _unirestResponse = UnirestResponse(response.code,
                                           response.headers,
                                           response.read())

    if callback is None or callback == {}:
        return _unirestResponse
    else:
        callback(_unirestResponse)

# The following methods in the Mashape class are based on
# Stripe's python bindings which are under the MIT license.
# See https://github.com/stripe/stripe-python



# End of Stripe methods.

HEADERS_KEY = 'headers'
CALLBACK_KEY = 'callback'
PARAMS_KEY = 'params'
AUTH_KEY = 'auth'


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
        url += utils.dict2query(dict((k, v) for k, v in params.iteritems() if v is not None))  # Removing None values/encode unicode objects

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


def __dorequest(method, url, params, headers, auth, callback=None):
    if callback is None:
        return __request(method, url, params, headers, auth)
    else:
        thread = threading.Thread(target=__request,
                                  args=(method,
                                        url,
                                        params,
                                        headers,
                                        auth,
                                        callback))
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
        self._body = self._raw_body

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
