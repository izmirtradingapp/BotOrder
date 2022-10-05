from flask import Flask, request
import json
from binance.client import Client
import math 


app = Flask(__name__)


@app.route("/webhook", methods=['POST'])
def webhook():

    def LongPosition(client,price,lev):
        assets = client.futures_account_balance()
        for asset in assets:
          if "BUSD" in asset.values():
            balance = float(asset["balance"])

        quot = math.floor((balance/price)*(95/100)*1000*lev)/1000

        params = {"symbol":"BTCBUSD",
                "type":"LIMIT",
                "side":"BUY",
                "price":price,
                "quantity":quot,
                "timeInForce":"GTC"}
        
        try:
            client.futures_cancel_all_open_orders(**{"symbol":"BTCBUSD"})
            ExitShortPosition(client)
            LongPos = client.futures_create_order(**params)
        except:
            client.futures_cancel_all_open_orders(**{"symbol":"BTCBUSD"})
            LongPos = client.futures_create_order(**params)
            
    def ExitLongPosition(client):
        qty = float(client.futures_position_information(symbol="BTCBUSD")[0]["positionAmt"])
        params = {
            "symbol":"BTCBUSD",
            "side":"SELL",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }

        client.futures_cancel_all_open_orders(**{"symbol":"BTCBUSD"})
        ExitLong = client.futures_create_order(**params)


    def ShortPosition(client,price,lev):
        assets = client.futures_account_balance()
        for asset in assets:
          if "BUSD" in asset.values():
            balance = float(asset["balance"])

        quot = math.floor((balance/price)*(95/100)*1000*lev)/1000

        params = {"symbol":"BTCBUSD",
                "type":"LIMIT",
                "side":"SELL",
                "price":price,
                "quantity":quot,
                "timeInForce":"GTC"}
        
        try:
            client.futures_cancel_all_open_orders(**{"symbol":"BTCBUSD"})
            ExitLongPosition(client)
            ShortPos = client.futures_create_order(**params)
        except:
            client.futures_cancel_all_open_orders(**{"symbol":"BTCBUSD"})
            ShortPos = client.futures_create_order(**params)

    def ExitShortPosition(client):
        qty = -(float(client.futures_position_information(symbol="BTCBUSD")[0]["positionAmt"]))
        params = {
            "symbol":"BTCBUSD",
            "side":"BUY",
            "type":'MARKET',
            "quantity":qty,
            "reduceOnly":"true"
            }
        client.futures_cancel_all_open_orders(**{"symbol":"BTCBUSD"})
        ExitShort = client.futures_create_order(**params)

    try:
        data = json.loads(request.data)
        order = data["order"]
        price = data["open"]
        lev = data["leverage"]
        api_key = data["api_key"]
        api_secret = data["api_secret"]
        
        client = Client(api_key, api_secret, testnet=False)
        client.futures_change_leverage(**{"symbol":"BTCBUSD","leverage":lev})

        if order == "LongPosition":
            LongPosition(client,price,lev)

        elif order == "ExitLongPosition":
            ExitLongPosition(client)
          
        elif order == "ShortPosition":
            ShortPosition(client,price,lev)

        elif order == "ExitShortPosition":
            ExitShortPosition(client)

    except Exception as e:
        print(e)
        pass
    return {
        "code": "success",

    }