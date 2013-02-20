from mashape.auth.header_auth import HeaderAuth
from mashape.http.auth_utils import AuthUtils


class MashapeAuth(HeaderAuth):

    def __init__(self, mashape_key):
        self.header.update(AuthUtils.generate_authentication_header(mashape_key))
