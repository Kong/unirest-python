Unicorn-Python
============================================

Unicorn is a set of lightweight HTTP libraries available in PHP, Ruby, Python, Java, Objective-C.

Documentation
-------------------

### Installing
To utilize unicorn, install the unicorn pip:

`pip install unicorn`

After installing the pip package you can now begin to simplifying requests by import:

`import unicorn`

### Creating Request
So you're probably wondering how using Unicorn makes creating requests in Python easier, let's start with a working example:

```python
response = unicorn.post("http://httpbin.org/post", { "Accept": "application/json" }, { "parameter": 23, "foo": "bar" })
```

### Asynchronous Requests
Python also has support for asynchronous requests in which you can define a `callback` to be passed along and invoked when Unicorn recieves the response.
For non-blocking requests in Python we need to define ourselves a callback to reference inside of our request method upon response:

```python
def callback(response):
  response.code # The HTTP status code
  response.headers # The HTTP headers
  response.body # The parsed response
  response.raw_body # The unparsed response
  
  thread = unicorn.post("http://httpbin.org/post", { "Accept": "application/json" }, { "parameter": 23, "foo": "bar" }, callback)
```

### File Uploads
Transferring file data requires that you `open` the file in a readable `r` mode:

```python
response = unicorn.post("http://httpbin.org/post", {"Accept": "application/json"},
  {
    "parameter": "value",
    "file": open("/tmp/file", mode="r")
  }
)
```

### Custom Entity Body

```python
import json

response = unicorn.post("http://httpbin.org/post", { "Accept": "application/json" },
  json.dumps({
    "parameter": "value",
    "foo": "bar"
  })
)
```
    
### Request Reference

```python
unicorn.get(url, headers = {}, callback = None)
unicorn.post(url, headers = {}, params = {}, callback = None)
unicorn.put(url, headers = {}, params = {}, callback = None)
unicorn.patch(url, headers = {}, params = {}, callback = None)    
unicorn.delete(url, headers = {}, callback = None)
```

`url`
Endpoint, address, or uri to be acted upon and requested information from.

`headers`
Request Headers as associative array or object

`body`
Request Body associative array or object

`callback`
Asychronous callback method to be invoked upon result.

### Response Reference
Upon recieving a response Unicorn returns the result in the form of an Object, this object should always have the same keys for each language regarding to the response details.

`code`
HTTP Response Status Code (Example 200)

`headers`
HTTP Response Headers

`body`
Parsed response body where applicable, for example JSON responses are parsed to Objects / Associative Arrays.

`raw_body`
Un-parsed response body

License
---------------

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
