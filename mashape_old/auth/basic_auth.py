from mashape.auth.auth import Auth
import base64


class BasicAuth(Auth):

    def __init__(self, username, password):
        headerVal = username + ":" + password
        self.header["Authorization"] = "Basic " + base64.b64encode(headerVal)
