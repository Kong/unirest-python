from mashape.auth.oauth_auth import OAuthAuth
from mashape.exception.client_exception import MashapeClientException
from mashape.exception.exception_messages import ExceptionMessages


class OAuth2Auth(OAuthAuth):

    def __init__(self, consumer_key, consumer_secret, callback_url):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.callback_url = callback_url

        self.headers["x-mashape-oauth-consumerkey"] = consumer_key
        self.headers["x-mashape-oauth-consumersecret"] = consumer_secret

    def handle_params(self):
        if self.access_token is None:
            raise MashapeClientException(
                    ExceptionMessages.EXCEPTION_OAUTH2_AUTHORIZE)

        params = {}
        params["accesstoken"] = self.accesstoken
        return params
