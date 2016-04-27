This repository is a fork of [Unirest Python](https://github.com/Mashape/unirest-python). 

# So, what's new ? Better exception handling.
* When making unirest requests, clients can provide a callback method to receive the response. Whenever a callback is provided, unirest creates a new thread to execute the request. By default, unirest only handles `urllib2.HTTPError` when making these requests, so in case of a `urllib2.URLError`, the program execution simply stops. This is especially difficult to catch when things are happening in another thread.  
* This fork adds the `urllib2.URLError` except clause to the try block. Since this exception does not have any HTTP Response code, the `UnirestResponse` object returned as a result has a response code of 0, an empty dict for headers and the error message from the exception.  
* If you wish to have a different response, update the `UnirestResponse` object [here](https://github.com/vshivam/unirest-python/blob/master/unirest/__init__.py#L103). 
* To be super safe, you can also add an except clause for `ValueError`. This exception will be thrown when the url is invalid e.g. no http:// prefix or blank. 
