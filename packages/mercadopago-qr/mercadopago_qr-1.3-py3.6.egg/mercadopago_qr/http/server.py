class server:
    # credentials
    client_id = None,
    client_secret = None,
    public_key = None,
    access_token = None,

    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 public_key=None,
                 access_token=None
                 ):

        self.client_id = client_id
        self.client_secret = client_secret
        self.public_key = public_key
        self.access_token = access_token  