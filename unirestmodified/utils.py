from poster.encode import multipart_encode
import urllib

def to_utf8(value):
    if isinstance(value, unicode):
        return urllib.quote_plus(value.encode('utf-8'))

    return value


def _dictionary_encoder(key, dictionary):
    result = []
    for k, v in dictionary.iteritems():
        if type(v) is file:
            continue
        key = to_utf8(key)
        k = to_utf8(k)
        v = to_utf8(v)
        result.append('{}[{}]={}'.format(key, k, v))

    return result


def dict2query(dictionary):
    """
    We want post vars of form:
    {'foo': 'bar', 'nested': {'a': 'b', 'c': 'd'}}
    to become:
    foo=bar&nested[a]=b&nested[c]=d
    """
    query = []
    encoders = {dict: _dictionary_encoder}
    for k, v in dictionary.iteritems():
        if v.__class__ in encoders:
            nested_query = encoders[v.__class__](k, v)
            query += nested_query
        else:
            key = to_utf8(k)
            value = to_utf8(v)
            query.append('{}={}'.format(key, value))

    return '&'.join(query)


def urlencode(data):
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, file):
                return multipart_encode(data)
        return dict2query(data), None
    else:
        return data, None


if __name__ == '__main__':
    print('...')
    print(dict2query({'foo': 'bar', 'nested': {'a': 'b', 'c': 'd'}}))
