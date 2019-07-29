def create_headers(token):
    return {
        'authorization': 'Bearer {}'.format(token),
        'content-type': 'application/json'
    }
