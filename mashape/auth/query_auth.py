from mashape.auth.auth import Auth


class QueryAuth(Auth):

    def __init__(self, query_key, query_value):
        self.params[query_key] = query_value
