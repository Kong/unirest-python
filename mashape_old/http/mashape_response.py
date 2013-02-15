import json
import urllib2


class MashapeResponse:
    
    def __init__(self, response, parse_json=True):
        self.raw_body = response.read()
        self.headers = response.info()
        self.code = response.getcode()

        if self.raw_body is not None and parse_json:
            self.body = json.loads(unicode(self.raw_body, errors='replace'))
        else:
            self.body = self.raw_body
