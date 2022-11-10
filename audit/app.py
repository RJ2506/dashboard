from time import strftime
import uuid
import connexion
from connexion import NoContent
import datetime
import requests
import json
import yaml
import logging, logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open("log_conf.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")

def get_purchase_item(index):
    """purchase the item you selected"""
    server = f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}'
    client = KafkaClient(hosts=server)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',reset_offset_on_start=True,consumer_timeout_ms=1000)

    logger.info("Retrieving buy at index %d" % index)
  
    try:
        for i,msg in enumerate(consumer):
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if i == index:
                return msg['payload'], 201
            else:
                raise ValueError
    except:
        logger.error("No more messages found")

   
    
    logger.error("Could not find buy at index %d" % index)

    return { "message": "Not Found"}, 404
def get_search_item(index):
    """purchase the item you selected"""
    server = f'{app_config["events"]["hostname"]}:{app_config["events"]["port"]}'
    client = KafkaClient(hosts=server)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    # Here we reset the offset on start so that we retrieve
    # messages at the beginning of the message queue.
    # To prevent the for loop from blocking, we set the timeout to
    # 100ms. There is a risk that this loop never stops if the
    # index is large and messages are constantly being received!
    consumer = topic.get_simple_consumer(reset_offset_on_start=True,consumer_timeout_ms=1000)

    logger.info("Retrieving buy at index %d" % index)

    try:
        for i,msg in enumerate(consumer):
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            if i == index:
                return msg['payload'], 201
            else:
                raise ValueError
    except:
        logger.error("No more messages found")

    logger.error("Could not find search at index %d" % index)

    return { "message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8110)