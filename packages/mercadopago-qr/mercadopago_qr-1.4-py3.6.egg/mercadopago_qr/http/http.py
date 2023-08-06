class http:
    _urls = {}

    def __init__(self, user_id=None, external_pos_id=None):        
        self._urls['secure_api'] = 'https://api.mercadopago.com'
        self._urls['unsecure_api'] = 'http://api.mercadopago.com'
        self._urls['qr'] = 'instore/orders/qr/seller/collectors/' + str(user_id) + '/pos/' + str(external_pos_id) + '/qrs'

    def get_endpoint(self, _key):
        if(_key in self._urls):
            return self._urls[_key]
        else:
            return None