from mashape.auth.header_auth import HeaderAuth
from mashape.http.auth_utils import AuthUtils


class MashapeAuth(HeaderAuth):

    def __init__(self, public_key, private_key):
        self.header.update(AuthUtils.generate_authentication_header(public_key,
            private_key))
