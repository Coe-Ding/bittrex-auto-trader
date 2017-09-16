from storage.storage_service import save_order_to_history
from .api_service import *
from storage.current_orders import current_orders


def create_sell_order(exchange, price, qnty, completed_orders):
    res = sell_limit(exchange, price, qnty)
    if res is not None and 'uuid' in res:
        save_order_to_history(exchange, current_orders[exchange]['Price'], qnty, 'BUY_LIMIT')
        save_order_to_history(exchange, price * 0.9975, qnty, 'SELL_LIMIT')
        completed_orders.append(exchange)


def place_sell_orders(gain):
    completed_orders = []
    open_exchanges = get_orders_exchanges()

    for exchange, values in current_orders.items():
        if exchange not in open_exchanges:
            create_sell_order(exchange, values['Price'] * gain, values['Quantity'], completed_orders)

    for order in completed_orders:
        del current_orders[order]


