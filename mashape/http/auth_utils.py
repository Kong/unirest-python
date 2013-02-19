
import hmac
import hashlib
import base64


class AuthUtils:

    @staticmethod
    def generate_authentication_header(mashape_key):
        return {"X-Mashape-Authorization":
                mashape_key}
