class http:
    _urls = {}

    def __init__(self, user_id=None, external_pos_id=None):        
        self._urls['api'] = 'https://api.mercadopago.com'
        self._urls['qr'] = 'instore/orders/qr/seller/collectors/{user_id}/pos/{external_pos_id}/qrs'

    def get_endpoint(self, _key):
        if(_key in self._urls):
            return self._urls[_key]
        else:
            return None