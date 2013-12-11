#!/usr/bin/env python2

import time
import key
import lib.cexapi as cexapi
import sys
import urllib2

api = cexapi.api('xatier', key.api_key, key.api_secret)

"""
official documentation is here: https://cex.io/api

the ticker object

    a dict of {last, high, low, volume, bid, ask}

        last     - last BTC price
        high     - last 24 hours price high
        low      - last 24 hours price low
        volume   - last 24 hours volume
        bid      - highest buy order
        ask      - lowest sell order

the order book (other people's but/sell record)

    a dict of {timestamp, bids{price, amount}, asks}


place order

    api.place_order(type, amount, price, couple = 'GHS/BTC')

        type   - 'buy' or 'sell'
        amount - amount
        price  - price

    returns

        {price, amount / time / type / id / pending}

"""
print("go!")


ticker = api.ticker('GHS/BTC')
#print("timestamp / last / bid / high / low")
#print("{} {} {} {} {}".format(ticker['timestamp'], ticker['last'],
#                              ticker['bid'], ticker['high'],
#                              ticker['low']))

last_price = float(ticker['last']) - 0.00025
try:

    while 1:
        try :
            order_book =  api.order_book('GHS/BTC')
        except Exception as e:
            print("Error occur{}".format(e))
            continue

        print(time.strftime("%b %d %H:%M:%S",
              time.localtime(int(order_book['timestamp']))))
        print("="*20)

        last_ten_order = order_book['bids'][0:10]
        for i in last_ten_order:
            p = i[0]
            print("    {}".format(float(p)))

        target_price = float(last_ten_order[2][0])

        print("="*20)
        print("target price @ {}".format(target_price))
        print("last price   @ {}".format(last_price))


        # new climbing up cycle
        if last_price - float(last_ten_order[0][0]) > 0.0015:
            print("[+] start a new cycle")
            last_price = target_price

        if target_price > last_price + 0.000000025:
            print("[+] should put an order @ {}".format(last_price))
            print("[+] earn {0:.9f} diff (yay)!!!".format(target_price -
                                                           last_price))
            new_order =  api.place_order('buy', 0.0001, last_price, 'GHS/BTC')
            #print("buy 0.00001 GHS at {}".format(new_order['price']))
            #print(new_order)
            last_price = target_price


        sys.stdout.flush()
        time.sleep(1)

except KeyboardInterrupt:
    print("bye")
