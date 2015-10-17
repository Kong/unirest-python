# Unirest for Python [![Build Status][travis-image]][travis-url] [![version][pypi-version]][pypi-url]

[![License][pypi-license]][license-url]
[![Downloads][pypi-downloads]][pypi-url]
[![Dependencies][versioneye-image]][versioneye-url]
[![Gitter][gitter-image]][gitter-url]

![][unirest-logo]


[Unirest](http://unirest.io) is a set of lightweight HTTP libraries available in multiple languages, built and maintained by [Mashape](https://github.com/Mashape), who also maintain the open-source API Gateway [Kong](https://github.com/Mashape/kong). 


## Features

* Make `GET`, `POST`, `PUT`, `PATCH`, `DELETE` requests
* Both syncronous and asynchronous (non-blocking) requests
* Supports form parameters, file uploads and custom body entities
* Supports gzip
* Supports Basic Authentication natively
* Customizable timeout
* Customizable default headers for every request (DRY)
* Automatic JSON parsing into a native object for JSON responses

## Installing
To utilize Unirest, install it using pip:

```bash
$ pip install unirest
```

After installing the pip package, you can now begin simplifying requests by importing unirest:

```python
import unirest
```

### Creating Requests

So you're probably wondering how using Unirest makes creating requests in Python easier, let's start with a working example:

```python
response = unirest.post("http://httpbin.org/post", headers={ "Accept": "application/json" }, params={ "parameter": 23, "foo": "bar" })

response.code # The HTTP status code
response.headers # The HTTP headers
response.body # The parsed response
response.raw_body # The unparsed response
```

## Asynchronous Requests

Python also supports asynchronous requests in which you can define a `callback` function to be passed along and invoked when Unirest receives the response:

```python
def callback_function(response):
  response.code # The HTTP status code
  response.headers # The HTTP headers
  response.body # The parsed response
  response.raw_body # The unparsed response
  
thread = unirest.post("http://httpbin.org/post", headers={ "Accept": "application/json" }, params={ "parameter": 23, "foo": "bar" }, callback=callback_function)
```

## File Uploads

Transferring file data requires that you `open` the file in a readable `r` mode:

```python
response = unirest.post("http://httpbin.org/post", headers={"Accept": "application/json"},
  params={
    "parameter": "value",
    "file": open("/tmp/file", mode="r")
  }
)
```

## Custom Entity Body

```python
import json

response = unirest.post("http://httpbin.org/post", headers={ "Accept": "application/json" },
  params=json.dumps({
    "parameter": "value",
    "foo": "bar"
  })
)
```

**Note**: For the sake of semplicity, even with custom entities in the body, the keyword argument is still `params` (instead of `data` for example). I'm looking for feedback on this.

### Basic Authentication

Authenticating the request with basic authentication can be done by providing an `auth` array like:

```python
response = unirest.get("http://httpbin.org/get", auth=('username', 'password'))
```
    
# Request

```python
unirest.get(url, headers = {}, params = {}, auth = (), callback = None)
unirest.post(url, headers = {}, params = {}, auth = (), callback = None)
unirest.put(url, headers = {}, params = {}, auth = (), callback = None)
unirest.patch(url, headers = {}, params = {}, auth = (), callback = None)    
unirest.delete(url, headers = {}, params = {}, auth = (), callback = None)
```

- `url` - Endpoint, address, or URI to be acted upon and requested information from in a string format.
- `headers` - Request Headers as an associative array
- `params` - Request Body as an associative array or object
- `auth` - The Basic Authentication credentials as an array
- `callback` - Asychronous callback method to be invoked upon result.

# Response
Upon receiving a response, Unirest returns the result in the form of an Object. This object should always have the same keys for each language regarding to the response details.

- `code` - HTTP Response Status Code (Example 200)
- `headers`- HTTP Response Headers
- `body`- Parsed response body where applicable, for example JSON responses are parsed to Objects / Associative Arrays.
- `raw_body`- Un-parsed response body

# Advanced Configuration

You can set some advanced configuration to tune Unirest-Python:

### Timeout

You can set a custom timeout value (in **seconds**):

```python
unirest.timeout(5) # 5s timeout
```

### Default Request Headers

You can set default headers that will be sent on every request:

```python
unirest.default_header('Header1','Value1')
unirest.default_header('Header2','Value2')
```

You can clear the default headers anytime with:

```python
unirest.clear_default_headers()
```

----

Made with &#9829; from the [Mashape](https://www.mashape.com/) team

[unirest-logo]: http://cl.ly/image/2P373Y090s2O/Image%202015-10-12%20at%209.48.06%20PM.png


[license-url]: https://github.com/Mashape/unirest-python/blob/master/LICENSE

[gitter-url]: https://gitter.im/Mashape/unirest-python
[gitter-image]: https://img.shields.io/badge/Gitter-Join%20Chat-blue.svg?style=flat

[travis-url]: https://travis-ci.org/Mashape/unirest-python
[travis-image]: https://img.shields.io/travis/Mashape/unirest-python.svg?style=flat

[pypi-url]: https://pypi.python.org/pypi/Unirest/
[pypi-license]: https://img.shields.io/pypi/l/Unirest.svg?style=flat
[pypi-version]: https://img.shields.io/pypi/v/Unirest.svg?style=flat
[pypi-downloads]: https://img.shields.io/pypi/dm/Unirest.svg?style=flat

[codeclimate-url]: https://codeclimate.com/github/Mashape/unirest-python
[codeclimate-quality]: https://img.shields.io/codeclimate/github/Mashape/unirest-python.svg?style=flat
[codeclimate-coverage]: https://img.shields.io/codeclimate/coverage/github/Mashape/unirest-python.svg?style=flat

[versioneye-url]: https://www.versioneye.com/user/projects/54b82a8905064657eb00024e
[versioneye-image]: https://img.shields.io/versioneye/d/user/projects/54b82a8905064657eb00024e.svg?style=flat

