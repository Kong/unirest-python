from __init__ import request

def get(url, headers = {}):
    return request("GET", url)