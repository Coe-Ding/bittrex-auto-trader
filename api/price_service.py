from api.api_service import get_order_history


def get_average_buy_price(exchange):
    total_price = 0
    total_qnty = 0

    for order in filter(lambda o: o['Exchange'] == exchange and o['OrderType'] == 'LIMIT_BUY', get_order_history()):
        total_price += order['Quantity'] * order['PricePerUnit']
        total_qnty += order['Quantity']

    if total_qnty == 0:
        return 0
    return total_price / total_qnty
