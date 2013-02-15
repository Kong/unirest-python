from mashape.auth.auth import Auth


class OAuthAuth(Auth):

    def __init__(self, consumer_key, consumer_secret, callback_url):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.callback_url = callback_url

    def get_oauth_base_params(self):
        params = {}

        params["consumerKey"] = self.consumer_key
        params["consumerSecret"] = self.consumer_secret
        params["callbackUrl"] = self.callback_url
        return params

    def add_access_token(self, access_token, access_secret=None):
        self.access_token = access_token
        self.access_secret = access_secret
