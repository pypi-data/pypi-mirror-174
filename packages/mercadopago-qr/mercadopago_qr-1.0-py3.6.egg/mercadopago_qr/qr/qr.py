from .. http.http import http
from .. http.server import server
from .. http.queries import queries
import logging
_logger = logging.getLogger(__name__)

class qr:

    def __init__(self):
        _logger.warning("init qr code service...")

    def validate(self, data):
        if(len(data) > 0):
            return True
        return False

    def generate_qr_code(self, params={}):
        qr_request = queries()
        url = http()
        endpoint = str(url.get_endpoint('api')) + str(url.get_endpoint('qr'))
        mercadopago = server(client_secret=params['client_secret'])
        headers = qr_request.get_headers_qr(mercadopago)
        params['headers'] = headers
        params['url'] = endpoint
        response = qr_request.post(params)
        return response