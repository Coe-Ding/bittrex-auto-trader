import time

from api.api_service import get_market_summaries, get_orders_exchanges
from api.buy_service import place_buy_orders, cancel_old_buys, cancel_all_buys
from api.sell_service import place_sell_orders

from storage.current_orders import current_orders
from storage.order_history import order_history
from storage.storage_service import save_data

# BUY AMOUNT (BTC)
BUY_AMOUNT = 0.0005

# PERCENT GAIN TO SELL AT
percent_gain = 0.02
trade_fee = 0.0025
GAIN = 1 + percent_gain + trade_fee

# ESTIMATED TIME TO RUN (MINUTES
RUN_TIME = 15

# CHOOSE MARKETS
MY_MARKETS = ['BTC-DASH', 'BTC-PPC', 'BTC-OMG', 'BTC-ARK', 'BTC-BAT',  'BTC-IOP', 'BTC-FUN', 'BTC-BAT',  'BTC-IOP', 'BTC-FUN', 'BTC-STRAT',
              'BTC-BNT', 'BTC-OMG', 'BTC-SYS', 'BTC-XMG', 'BTC-QTUM', 'BTC-ETC']


def should_buy(m, open_exchanges):
    # m['BaseVolume'] > 2500
    return m['MarketName'] not in current_orders and m['MarketName'] not in open_exchanges and m['MarketName'] in MY_MARKETS


def get_buy_markets():
    open_exchanges = get_orders_exchanges()
    return filter(lambda m: should_buy(m, open_exchanges), get_market_summaries())


def start_trading():
    if len(current_orders.keys()) > 0:
        cancel_old_buys()
        place_sell_orders(GAIN)

    time.sleep(1)
    place_buy_orders(get_buy_markets(), BUY_AMOUNT)


def run():
    print('running... ')

    iterations = RUN_TIME * 60 / 4.3
    start_time = time.time()

    for x in range(0, int(iterations)):
        start_trading()

        if x % 10 == 0 and x != 0:
            time_taken = time.time() - start_time
            total_time = time_taken / x * iterations
            print('run', x + 1, 'of', iterations, 'minutes:', round(time_taken / 60, 2), 'remaining:', round((total_time - time_taken) / 60, 2), '\n')

        time.sleep(1)

    if len(current_orders.keys()) > 0:
        cancel_old_buys()
        place_sell_orders(GAIN)

    print('Completed in ', round((time.time() - start_time) / 60, 2), 'mins')


run()
# cancel_all_buys()
save_data('current_orders', current_orders)
save_data('order_history', order_history)



