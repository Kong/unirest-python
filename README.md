# Unirest for Python

Unirest is a set of lightweight HTTP libraries in multiple languages.

## Installing
To utilize unirest, install the unirest pip:

`pip install unirest`

After installing the pip package you can now begin to simplifying requests by import:

`import unirest`

### Creating Request
So you're probably wondering how using Unirest makes creating requests in Python easier, let's start with a working example:

```python
response = unirest.post("http://httpbin.org/post", { "Accept": "application/json" }, { "parameter": 23, "foo": "bar" })
```

## Asynchronous Requests
Python also has support for asynchronous requests in which you can define a `callback` to be passed along and invoked when Unirest recieves the response.
For non-blocking requests in Python we need to define ourselves a callback to reference inside of our request method upon response:

```python
def callback(response):
  response.code # The HTTP status code
  response.headers # The HTTP headers
  response.body # The parsed response
  response.raw_body # The unparsed response
  
  thread = unirest.post("http://httpbin.org/post", { "Accept": "application/json" }, { "parameter": 23, "foo": "bar" }, callback)
```

## File Uploads
Transferring file data requires that you `open` the file in a readable `r` mode:

```python
response = unirest.post("http://httpbin.org/post", {"Accept": "application/json"},
  {
    "parameter": "value",
    "file": open("/tmp/file", mode="r")
  }
)
```

## Custom Entity Body

```python
import json

response = unirest.post("http://httpbin.org/post", { "Accept": "application/json" },
  json.dumps({
    "parameter": "value",
    "foo": "bar"
  })
)
```
    
# Request

```python
unirest.get(url, headers = {}, callback = None)
unirest.post(url, headers = {}, params = {}, callback = None)
unirest.put(url, headers = {}, params = {}, callback = None)
unirest.patch(url, headers = {}, params = {}, callback = None)    
unirest.delete(url, headers = {}, callback = None)
```

- `url` - Endpoint, address, or uri to be acted upon and requested information from.
- `headers` - Request Headers as associative array or object
- `body` - Request Body associative array or object
- `callback` - Asychronous callback method to be invoked upon result.

# Response
Upon recieving a response Unirest returns the result in the form of an Object, this object should always have the same keys for each language regarding to the response details.

- `code` - HTTP Response Status Code (Example 200)
- `headers`- HTTP Response Headers
- `body`- Parsed response body where applicable, for example JSON responses are parsed to Objects / Associative Arrays.
- `raw_body`- Un-parsed response body
