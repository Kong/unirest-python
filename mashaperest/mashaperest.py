from __init__ import request
import threading

def get(url, headers = {}, callback = None):
    return __dorequest("GET", url, {}, headers, callback)
    
def post(url, params = {}, headers = {}, callback = None):
    return __dorequest("POST", url, params, headers, callback)
    
def put(url, params = {}, headers = {}, callback = None):
    return __dorequest("PUT", url, params, headers, callback)
    
def delete(url, params = {}, headers = {}, callback = None):
    return __dorequest("DELETE", url, params, headers, callback)
    
def patch(url, params = {}, headers = {}, callback = None):
    return __dorequest("PATCH", url, params, headers, callback)
    
def __dorequest(method, url, params, headers, callback = None):
    if callback is None:
        return request(method, url, params, headers)
    else:
        return threading.Thread(target=request, args=(method, url, params, headers, callback)).start()