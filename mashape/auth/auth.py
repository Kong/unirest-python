class Auth(object):

    header = {}
    params = {}

    def handle_headers(self):
        return self.header

    def handle_params(self):
        return self.params
