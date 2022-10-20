import http.client
import json
from urllib.parse import urlencode

class Single :

    # Properties
    def __init__(self, secret) :
        self.secret = secret

    def execute(self, indicator, exchange, symbol, interval, params = {}) :
        conn = http.client.HTTPSConnection("api.taapi.io")

        params.update({
            "secret": self.secret,
            "exchange": exchange,
            "symbol": symbol,
            "interval": interval,
        })

        query = "/"+indicator+"?"+urlencode(params)

        #print(query)

        payload = ""

        headers = { 'Content-Type': "application/json" }

        conn.request("GET", query, payload, headers)

        res = conn.getresponse()
        data = res.read()

        result = json.loads(data.decode("utf-8"))

        print(result["value"])
    
    