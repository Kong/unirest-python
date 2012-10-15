from mashape.auth.oauth_auth import OAuthAuth
from mashape.exception.client_exception import MashapeClientException
from mashape.exception.exception_messages import ExceptionMessages


class OAuth2Auth(OAuthAuth):

    def __init__(self, consumer_key, consumer_secret, callback_url):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.callback_url = callback_url
        self.access_token = None

    def handle_params(self, url):
        params = {}
        
        if url.endswith("/oauth_url"):
            params["consumerKey"] =  self.consumer_key
            params["consumerSecret"] = self.consumer_secret
            params["callbackUrl"] = self.callback_url
        else:
            if self.access_token is None:
                raise MashapeClientException(
                        ExceptionMessages.EXCEPTION_OAUTH2_AUTHORIZE)

            params["access_token"] = self.access_token
        return params
