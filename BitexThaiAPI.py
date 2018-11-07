
import requests
import json
import base64
import hmac
import hashlib
import time

class BXinth:
        def __init__(self, publ,secret):
                self.API_KEY=publ
                self.API_SECRET=secret
                self.URL = "https://bx.in.th/api/"

        def market_data(self):

            r = requests.get(self.URL)

            return r

        def symbols(self): # get a list of valid symbol IDs.

                r = requests.get(self.URL + "pairing/")
                rep = r.json()

                return rep

        def lends(self, currency='1'): # get a list of the most recent lending data for the given currency: total amount lent and rate (in % by 365 days).

                r = requests.get(self.URL + "trade/?pairing=" + currency)
                rep = r.json()

                return rep
        
        def orderbook(self, symbol='1'): # get the full order book.

                r = requests.get(self.URL + "orderbook/?pairing=" + symbol)
                rep = r.json()

                return rep



        def genNonce(self): # generates a nonce, used for authentication.
                return str(int(time.time() * 1000000))

        def payloadPacker(self, payload): # packs and signs the payload of the request.

                non=payload["nonce"]
                j = json.dumps(payload)
                data = base64.b64encode(j.encode())

                h = hmac.new(self.API_SECRET.encode(), data, hashlib.sha256)
                signature = h.hexdigest()

                return {
                        "key": self.API_KEY,
                        "nonce": non,
                        "signature": signature
                }

        def place_order(self, amount, price, side, ord_type, symbol='btcusd', exchange='bitfinex'): # submit a new order.

                payload = {

                        "request":"/v1/order/new",
                        "nonce":self.genNonce(),
                        "symbol":symbol,
                        "amount":amount,
                        "price":price,
                        "exchange":exchange,
                        "side":side,
                        "type":ord_type

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/order/new", headers=signed_payload, verify=True)
                rep = r.json()

                try:
                        rep['order_id']
                except:
                        return rep['message']

                return rep

        def delete_order(self, order_id): # cancel an order.

                payload = {

                        "request":"/v1/order/cancel",
                        "nonce":self.genNonce(),
                        "order_id":order_id

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/order/cancel", headers=signed_payload, verify=True)
                rep = r.json()

                try:
                        rep['avg_execution_price']
                except:
                        return rep['message']

                return rep

        def delete_all_order(self): # cancel an order.

                payload = {

                        "request":"/v1/order/cancel/all",
                        "nonce":self.genNonce(),

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/order/cancel/all", headers=signed_payload, verify=True)
                rep = r.json()
                return rep
        '''
                try:
                        rep['avg_execution_price']
                except:
                        return rep['message']
        '''

        def status_order(self, order_id): # get the status of an order. Is it active? Was it cancelled? To what extent has it been executed? etc.

                payload = {

                        "request":"/v1/order/status",
                        "nonce":self.genNonce(),
                        "order_id":order_id

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/order/status", headers=signed_payload, verify=True)
                rep = r.json()

                try:
                        rep['avg_execution_price']
                except:
                        return rep['message']

                return rep

        def active_orders(self): # view your active orders.

                payload = {

                        "request":"/v1/orders",
                        "nonce":self.genNonce()

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/orders", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def active_positions(self): # view your active positions.

                payload = {

                        "request":"/v1/positions",
                        "nonce":self.genNonce()

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/positions", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def claim_position(self, position_id): # Claim a position.

                payload = {

                        "request":"/v1/position/claim",
                        "nonce":self.genNonce(),
                        "position_id":position_id

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/position/claim", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def close_position(self, position_id): # Claim a position.

                payload = {

                        "request":"/v1/position/close",
                        "nonce":self.genNonce(),
                        "position_id":position_id

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/position/close", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def past_trades(self, timestamp=0, symbol='btcusd'): # view your past trades

                payload = {

                        "request":"/v1/mytrades",
                        "nonce":self.genNonce(),
                        "symbol":symbol,
                        "timestamp":timestamp

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/mytrades", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def place_offer(self, currency, amount, rate, period, direction):

                payload = {

                        "request":"/v1/offer/new",
                        "nonce":self.genNonce(),
                        "currency":currency,
                        "amount":amount,
                        "rate":rate,
                        "period":period,
                        "direction":direction

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/offer/new", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def cancel_offer(self, offer_id):

                payload = {

                        "request":"/v1/offer/cancel",
                        "nonce":self.genNonce(),
                        "offer_id":offer_id

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/offer/cancel", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def status_offer(self, offer_id):

                payload = {

                        "request":"/v1/offer/status",
                        "nonce":self.genNonce(),
                        "offer_id":offer_id

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/offer/status", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def active_offers(self):

                payload = {

                        "request":"/v1/offers",
                        "nonce":self.genNonce()

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/offers", headers=signed_payload, verify=True)
                rep = r.json()

                return rep

        def balances(self): # see your balances.

                payload = {
                        
                        "nonce":self.genNonce()

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "balances/", headers=signed_payload)
                rep = r.json()

                return rep

        def withdraw(self, withdraw_type, walletselected, amount, address):

                payload = {

                        "request":"/v1/withdraw",
                        "nonce":self.genNonce(),
                        "withdraw_type":withdraw_type,
                        "walletselected":walletselected,
                        "amount":amount,
                        "address":address

                }

                signed_payload = self.payloadPacker(payload)
                r = requests.post(self.URL + "/withdraw", headers=signed_payload, verify=True)
                rep = r.json()

                return rep
