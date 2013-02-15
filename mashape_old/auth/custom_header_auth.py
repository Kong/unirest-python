from mashape.auth.header_auth import HeaderAuth


class CustomHeaderAuth(HeaderAuth):

    def __init__(self, header_name, header_value):
        self.header[header_name] = header_value
