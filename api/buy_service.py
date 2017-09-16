from api.api_service import *
from storage.current_orders import current_orders
from storage.storage_service import save_order_to_history


def create_buy_order(exchange, price, qnty, buy_amount):
    res = buy_limit(exchange, price, qnty)
    if res is not None and 'uuid' in res:
        print('BUY ORDER PLACED', qnty, exchange, 'at', price, ' Total: ', buy_amount, '\n')
        current_orders[exchange] = {'Quantity': qnty, 'Price': price, 'Total': buy_amount, 'OrderUuid': res['uuid'], 'Time': time.time()}


def place_buy_orders(markets, buy_amount):
    for market in markets:
        price = float(market['Bid']) * 1.001
        qnty = buy_amount / price
        create_buy_order(market['MarketName'], price, qnty - qnty * 0.0024, buy_amount)


def get_open_buys():
    # o['Exchange'] in current_orders and 
    return filter(lambda o: o['OrderType'] == 'LIMIT_BUY', get_open_orders())


# CANCEL
def cancel_buy(order, exchange, qnty, remaining):
    cancel_order(order['OrderUuid'])

    if qnty != remaining:
        save_order_to_history(exchange, order['Price'], qnty - remaining, 'BUY_LIMIT')

    print('CANCELLED BUY ORDER', exchange, 'qnty:', remaining, '\n')
    del current_orders[exchange]


def cancel_all_buys():
    for order in get_open_buys():
        if cancel_order(order['OrderUuid']):
            del current_orders[order['Exchange']]
    print('all buys deleted')


def order_is_old(exchange):
    return (time.time() - current_orders[exchange]['Time']) / 60 > 2


def cancel_old_buys():
    for order in get_open_buys():
        exchange = str(order['Exchange'])

        if exchange in current_orders and order_is_old(exchange):
            cancel_buy(current_orders[exchange], exchange, order['Quantity'], order['QuantityRemaining'])
