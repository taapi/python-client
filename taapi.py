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

        return result
    
    
class Bulk :

    # Properties
    def __init__(self, secret) :
        self.secret = secret
        self.outputFormat = "objects"
        self.constructs = []

    # Reset constructs
    def initConstructs(self) :
        self.constructs = []

    # Set output format [default, objects]
    def setOutputFormat(self, outputFormat) :
        self.outputFormat = outputFormat

    # Add a construct
    def addConstruct(self, construct) :
        self.constructs.append(construct.generate())

    # Execute: calculate indicator values
    def execute(self) :
        
        query = json.dumps({
            "secret": self.secret,
            "outputFormat": self.outputFormat,
            "construct": self.constructs[0] if len(self.constructs) == 1 else self.constructs
        })

        conn = http.client.HTTPSConnection("api.taapi.io")

        headers = { 'Content-Type': "application/json" }

        conn.request("POST", "/bulk", query, headers)

        res = conn.getresponse()
        data = res.read()

        result = json.loads(data.decode("utf-8"))

        return result
    
class Construct :

    # Constructor
    def __init__(self, exchange, symbol, interval) :
        self.exchange = exchange;
        self.symbol = symbol;
        self.interval = interval;
        self.indicators = []

    # Reset indicators
    def initIndicators(self) :
        self.indicators = []

    # Add an indicator along with parameters
    def addIndicator(self, indicator, params = {}) :

        params.update({
            "indicator": indicator
        })

        self.indicators.append(params)

    # Generate construct
    def generate(self) :
        construct = {
            "exchange": self.exchange,
            "symbol": self.symbol,
            "interval": self.interval,
            "indicators": self.indicators
        }

        return construct