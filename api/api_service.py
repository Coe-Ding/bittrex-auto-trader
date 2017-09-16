from .api_base import *


# PUBLIC
def get_market_summaries():
    return make_api_request('public/getmarketsummaries', '')


# ACCOUNT
def get_balances():
    return make_api_auth_request('account/getbalances', '')


def get_order_history():
    return make_api_auth_request('account/getorderhistory', '')


def get_balance():
    res = make_api_auth_request('account/getbalance', '&currency=BTC')
    if res is not None and 'Balance' in res:
        return res['Balance']


# MARKET
def buy_limit(market, price, qnty):
    return make_api_auth_request('market/buylimit', '&market=' + market + '&quantity=' + str(qnty) + '&rate=' + str(price))


def sell_limit(market, price, qnty):
    return make_api_auth_request('market/selllimit', '&market=' + market + '&quantity=' + str(qnty) + '&rate=' + str(price))


def cancel_order(uuid):
    return make_api_auth_request('market/cancel', '&uuid=' + str(uuid))


def get_open_orders():
    return make_api_auth_request('market/getopenorders', '')


def get_orders_exchanges():
    orders = []
    open_orders = make_api_auth_request('market/getopenorders', '')

    if open_orders is not None:
        for order in open_orders:
            orders.append(order['Exchange'])

    return orders


