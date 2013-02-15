from __init__ import request

def get(url, headers = {}):
    return request("GET", url, {}, headers)
    
def post(url, params = {}, headers = {}):
    return request("POST", url, params, headers)
    
def put(url, params = {}, headers = {}):
    return request("PUT", url, params, headers)
    
def delete(url, params = {}, headers = {}):
    return request("DELETE", url, params, headers)
    
def patch(url, params = {}, headers = {}):
    return request("PATCH", url, params, headers)