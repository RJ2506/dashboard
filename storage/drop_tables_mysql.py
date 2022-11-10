import mysql.connector

conn = mysql.connector.connect(
    user="RJ", password="Rodolfjohn25!", host="acit3855-kafka-lab6a.eastus.cloudapp.azure.com", database="kafka"
)

c = conn.cursor()
c.execute(
    """
    DROP TABLE buying_products;
    DROP TABLE search_products;
    """
)


conn.close()
