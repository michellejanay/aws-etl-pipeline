# This file exists to separate the direct use of psycopg2 in 'connect_to_db.py'
# from functions here that only care about the Connection and Cursor - this makes these easier to unit test.

import logging
import uuid
# lines 4,7 and 8 we are setting it up so we can log to cloudwatch
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def write_products(data, connection, cursor):
    all_orders = []
    seen = set()
    menu_items = []
    for item in data:
        for product in item['item_purchased']:
            all_orders.append(product)
    for products_dict in all_orders:
        products_tuple = tuple(products_dict.items())
        if products_tuple not in seen:
            seen.add(products_tuple)
            menu_items.append(products_dict)

    for item in menu_items:
        products_id = str(uuid.uuid4())
        sql=f"""SELECT EXISTS(SELECT 1 FROM products WHERE product_name='{item['name']}')"""
        cursor.execute(sql)
        result = cursor.fetchone()[0]

        if result:
            continue
        else:
            sql= f"""
                INSERT into products (product_id, product_name, price) VALUES ('{products_id}','{item['name']}', {float(item['price'])});
                """
            cursor.execute(sql)
    connection.commit()
    


def write_transactions_and_ordered_products(data, connection, cursor):
    for item in data: 
        transaction_id = str(uuid.uuid4())
        transaction_sql= f"""
            INSERT into transactions (transaction_id, "timestamp", total_amount, payment_method, store_name) VALUES ('{transaction_id}','{item['Timestamp']}', {float(item['total_amount'])}, '{item['payment_method']}', '{item['location']}');
            """
        cursor.execute(transaction_sql)

        products = item['item_purchased']
        for item in products: 
            product_sql = f"""
            SELECT product_id, price FROM products WHERE product_name = '{item['name']}';
            """
            cursor.execute(product_sql)
            products = cursor.fetchone()
            product_id = products[0]

            ordered_product_sql = f"""
                INSERT INTO ordered_products (transaction_id, product_id, product_quantity)
                VALUES ('{transaction_id}', '{product_id}', {item['quantity']});
                """
            cursor.execute(ordered_product_sql)
    connection.commit()
    

# we are passing in the connection and the cursor to be able to connect to the database.
def create_db_tables(connection, cursor):

    LOGGER.info("create_db_tables: started")
    try:
        sql_commands = """
        CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR (50) UNIQUE NOT NULL PRIMARY KEY, 
        product_name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
);
        CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR (50) UNIQUE NOT NULL PRIMARY KEY,      
        "timestamp" TIMESTAMP,
        total_amount DECIMAL(10, 2) NOT NULL,
        payment_method VARCHAR(100),                      
        store_name VARCHAR(100)
);
        CREATE TABLE IF NOT EXISTS ordered_products (
        transaction_id VARCHAR (50) NOT NULL,
        product_id VARCHAR (50) NOT NULL,
        product_quantity INT NOT NULL,
        PRIMARY KEY (transaction_id, product_id),
        FOREIGN KEY (transaction_id)
        REFERENCES transactions (transaction_id),
        FOREIGN KEY (product_id)
        REFERENCES products (product_id)
);
"""
        LOGGER.info("create_db_tables: creating tables")
        cursor.execute(sql_commands)

        LOGGER.info("create_db_tables: committing")
        connection.commit()

        LOGGER.info("create_db_tables: done")
    except Exception as ex:
        LOGGER.info(f"create_db_tables: failed to run sql: {ex}")
        raise ex



# we are writing a function to save the information in out newly created database tables 
def save_data_in_db(connection, cursor, bucket_name, file_path, data):
    LOGGER.info(f'save_data_in_db: started: file_path={file_path}, rows={len(data)}')

    try:
        LOGGER.info(f'write_products: started')
        write_products(data, connection, cursor)
        LOGGER.info(f'write_transactions_and_ordered_products: started')
        write_transactions_and_ordered_products(data,connection, cursor)

        LOGGER.info(f'save_data_in_db: done: file_path={file_path}, rows={len(data)}')
    except Exception as ex:
        LOGGER.info(f'save_data_in_db: error: ex={ex}, file_path={file_path}')
        raise ex