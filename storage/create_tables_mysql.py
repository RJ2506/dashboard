import mysql.connector

conn = mysql.connector.connect(
    user="RJ", password="Rodolfjohn25!", host="acit3855-kafka-lab6a.eastus.cloudapp.azure.com", database="kafka"
)


# Creating a cursor object using the cursor() method
c = conn.cursor()
c.execute(
    """
          CREATE TABLE buying_products
          (id integer PRIMARY KEY AUTO_INCREMENT , 
           credit_card BIGINT(16) NOT NULL,
           customer_id VARCHAR(250) NOT NULL,
           price FLOAT NOT NULL,
           transaction_number VARCHAR(100) NOT NULL,
           purchased_date VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           trace_id VARCHAR(250) NOT NULL)
          """
)

c.execute(
    """
          CREATE TABLE search_products
          (id integer PRIMARY KEY AUTO_INCREMENT, 
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

# Closing the connection
conn.commit()
conn.close()
