from mashape.auth.auth import Auth


class HeaderAuth(Auth):

    def handle_params(self):
        return None
