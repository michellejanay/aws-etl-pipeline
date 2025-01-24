import csv
from datetime import datetime
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def extract_csv(body_text):
    extracted_data = []
    LOGGER.info('extract: starting')

    headers = ['Timestamp','location','customer_name','item_purchased','total_amount','payment_method','card_num']
    csv_reader = csv.DictReader(body_text, fieldnames=headers, delimiter=',',)
    for row in csv_reader:
        extracted_data.append(row)
    LOGGER.info(f'extract: done: rows={len(extracted_data)}')
    return extracted_data
    
def remove_ppi(data):
    LOGGER.info(f'remove_ppi: processing={len(data)}')
    for item in data:
        item.pop("customer_name", None)
        item.pop("card_num", None)
    LOGGER.info(f'remove_ppi: done')   
    return data

def transform_timestamp(data):
    LOGGER.info(f'transform_timestamp: starting')
    for item in data:
        timestamp = item['Timestamp']
        converted_timestamp = datetime.strptime(timestamp, '%d/%m/%Y %H:%M')
        item['Timestamp'] = converted_timestamp
    LOGGER.info(f'transform_timestamp: done')  
    return data

def transform_orders(data):
    LOGGER.info(f'transform_orders: starting')
    data = remove_ppi(data)
    split_data = []
    result = []
    for item in data: 
        split_orders = item['item_purchased'].split(',')
        split_data.append(split_orders)
    for item in split_data:
        basket = []
        for product_list in item:
            order_split = product_list.rsplit('-', 1)
            order_dict = {'name': order_split[0].strip(), 'price': float(order_split[1].strip())}
            basket.append(order_dict) 
        result.append(basket)
    for index in range(len(data)):
        data[index]['item_purchased'] = result[index]
    LOGGER.info(f'transform_orders: done')
    return data

def update_order_quantity(data):
    LOGGER.info(f'update_orders_quantity: starting')
    for order in data:
        product_dict = {}
        for product in order['item_purchased']:
            product_key = (product['name'], product['price'])
            if product_key in product_dict:
                product_dict[product_key]['quantity'] += 1
            else:
                product_dict[product_key] = {**product, 'quantity': 1}
        order['item_purchased'] = list(product_dict.values())
    LOGGER.info(f'update_orders_quantity: done')   
    return data

def transform_data(data):
    LOGGER.info(f'transform data: starting')  
    data = remove_ppi(data)
    data = transform_timestamp(data)
    data = transform_orders(data)
    data = update_order_quantity(data)
    LOGGER.info(f'transform data: done')  
    return data

