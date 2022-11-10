import sqlite3

conn = sqlite3.connect("readings.sqlite")

c = conn.cursor()
c.execute(
    """
          CREATE TABLE buying_products
          (id INTEGER PRIMARY KEY ASC, 
           credit_card integer(16) NOT NULL,
           customer_id VARCHAR(250) NOT NULL,
           price FLOAT NOT NULL,
           transaction_number VARCHAR(100) NOT NULL,
           purchased_date VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL)
          """
)
#

c.execute(
    """
          CREATE TABLE search_products
          (id INTEGER PRIMARY KEY ASC, 
           brand_name VARCHAR(250) NOT NULL,
           item_description VARCHAR(250) NOT NULL,
           price FLOAT NOT NULL,
           product_name VARCHAR(250) NOT NULL,
           quantity_left INTEGER NOT NULL,
           sales_price FLOAT NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL)
          """
)

conn.commit()
conn.close()
