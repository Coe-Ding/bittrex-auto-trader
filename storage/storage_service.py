import time

from .order_history import order_history


def save_order_to_history(exchange, price, qnty, order_type):
    total = qnty * price if order_type == 'SELL_LIMIT' else qnty * price * 0.0025
    o = {'Exchange': exchange, 'Quantity': qnty, 'Price': price, 'Total': total, 'OrderType': order_type, 'Time': time.time()}
    order_history.append(o)
    print('\n', order_type, qnty, exchange, 'at', price, 'Total:',  total)


def append_data(name, data):
    with open(name, 'a') as f:
        f.write(str(data))
    print('Saved', name, '\n')


def save_data(name, data):
    with open('storage/' + name + '.py', 'w') as f:
        f.write(str(name + ' = ' + str(data)))

    print('Saved', name, '\n')
