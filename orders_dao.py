from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO 'order' "
             "(customer_name, total, datetime)"
             "VALUES (%s, %s, %s)")
    order_data = (order['customer_name'], order['grand_total'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    orders_details_query = ("INSERT INTO orders_details "
                           "(order_id, product_id, quantity, total_price)"
                           "VALUES (%s, %s, %s, %s)")
    orders_details_data = []
    for orders_detail_record in order['orders_details']:
        orders_details_data.append([
            order_id,
            int(orders_detail_record['product_id']),
            float(orders_detail_record['quantity']),
            float(orders_detail_record['total_price'])
        ])
    cursor.executemany(orders_details_query, orders_details_data)

    connection.commit()

    return order_id

def get_orders_details(connection, order_id):
    cursor = connection.cursor()

    query = "SELECT * from orders_details where order_id = %s"

    query = "SELECT orders_details.order_id, orders_details.quantity, orders_details.total_price, "\
            "products.name, products.price_per_unit FROM orders_details LEFT JOIN products on " \
            "orders_details.product_id = products.products_id where orders_details.order_id = %s"

    data = (order_id, )

    cursor.execute(query, data)

    records = []
    for (order_id, quantity, total_price, product_name, price_per_unit) in cursor:
        records.append({
            'order_id': order_id,
            'quantity': quantity,
            'total_price': total_price,
            'product_name': product_name,
            'price_per_unit': price_per_unit
        })

    cursor.close()

    return records

def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM `order`")
    cursor.execute(query)
    print("hello")
    print(cursor)
    response = []
    for (order_id, customer_name, total, dt) in cursor:
        response.append({
            'order_id': order_id,
            'customer_name': customer_name,
            'total': total,
            'datetime': dt,
        })

    cursor.close()

    # append order details in each order
    for record in response:
        record['orders_details'] = get_orders_details(connection, record['order_id'])

    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(get_orders_details(connection,4))
    # print(insert_order(connection, {
    #     'customer_name': 'dhaval',
    #     'total': '500',
    #     'datetime': datetime.now(),
    #     'orders_details': [
    #         {
    #             'product_id': 1,
    #             'quantity': 2,
    #             'total_price': 50
    #         },
    #         {
    #             'product_id': 3,
    #             'quantity': 1,
    #             'total_price': 30
    #         }
    #     ]
    # }))