from platform import python_branch
from sqlite3 import connect
import requests
import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from search import SearchProducts
from buy import BuyingProducts
import pymysql
import mysql.connector
import yaml, logging, logging.config
import datetime
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread
import json

with open("app_conf.yaml", "r") as f:
    app_config = yaml.safe_load(f.read())


with open("log_conf.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")

logger.info(f'Connecting to DB, Hostname:{app_config["datastore"]["hostname"]}, Port:{app_config["datastore"]["port"]}')

DB_ENGINE = create_engine(
    f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}'
)
# DB_ENGINE = create_engine(
#     f'mysql+pymysql://rj:Rodolfjohn25!@localhost:3306/mydb'
# )

# DB_ENGINE = create_engine("sqlite:///book.sqlite")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_purchase_item(timestamp):
    """get the  timestamp of the purchase tiem"""
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(BuyingProducts).filter(BuyingProducts.date_created >= timestamp_datetime)

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    
    
    session.close()
    logger.info(
        "Query for purchase item after %s returns %d results"
        % (timestamp, len(results_list))
    )

    return results_list, 200

def get_search_item(timestamp):
    """get the  timestamp of the purchase tiem"""
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    readings = session.query(SearchProducts).filter(
        SearchProducts.date_created >= timestamp_datetime
    )

    results_list = []

    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info(
        "Query for Search Items after %s returns %d results"
        % (timestamp, len(results_list))
    )

    return results_list, 200

def process_messages():
 """ Process event messages """
 hostname = "%s:%d" % (app_config["events"]["hostname"],app_config["events"]["port"])
 client = KafkaClient(hosts=hostname)
 topic = client.topics[str.encode(app_config["events"]["topic"])]

 # Create a consume on a consumer group, that only reads new messages

 # (uncommitted messages) when the service re-starts (i.e., it doesn't
 # read all the old messages from the history in the message queue).
 consumer = topic.get_simple_consumer(consumer_group=b'event_group',reset_offset_on_start=False,auto_offset_reset=OffsetType.LATEST)
 # This is blocking - it will wait for a new message
 for msg in consumer:
    msg_str = msg.value.decode('utf-8')
    msg = json.loads(msg_str)
    logger.info("Message: %s" % msg)
    payload = msg["payload"]

    if msg["type"] == "purchase": # Change this to your event type
        # Store the event1 (i.e., the payload) to the DB
        session = DB_SESSION()
        bp = BuyingProducts(
            payload["customer_id"],
            payload["credit_card"],
            payload["price"],
            payload["purchased_date"],
            payload["transaction_number"],
            payload["trace_id"],
        )
        session.add(bp)
        session.commit()
        session.close()
    elif msg["type"] == "search": # Change this to your event type
        # Store the event2 (i.e., the payload) to the DB
        session = DB_SESSION()

        sp = SearchProducts(
            payload["brand_name"],
            payload["item_description"],
            payload["price"],
            payload["product_name"],
            payload["quantity_left"],
            payload["sales_price"],
            payload["trace_id"],
        )
        session.add(sp)
        session.commit()
        session.close()
    # Commit the new message as being read
    consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages())
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
