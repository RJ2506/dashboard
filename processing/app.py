from sqlite3 import  connect
import requests
import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from stats import Stats
from base import Base

import yaml, logging, logging.config
import datetime
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler





DB_ENGINE = create_engine("sqlite:///stats.sqlite")

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

with open("app_conf.yaml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open("log_conf.yaml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    
logger = logging.getLogger("basicLogger")


def get_stats():
    """get the stats from storage application"""
    session = DB_SESSION()
    time = datetime.datetime.now()
    readings = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    
    if readings == None:
        ss = Stats(5,6,100, 200, 10,10, time)
        session.add(ss)
        session.commit()
        session.close()
        return None

    else:
        result = readings.to_dict()
        session.close()    
        return result, 201

def populate_stats():
    """ periodically update stats """
    session = DB_SESSION()
    time = datetime.datetime.now()
    result = session.query(Stats).order_by(Stats.last_updated.desc()).first()
    

    if result == None:
        Stats(5,6,100, 200, 10,10, time)
    else:
        last_updated = result.last_updated
        last_updated_format = str(last_updated.strftime("%Y-%m-%dT%H:%M:%SZ"))
        res_buy = requests.get(app_config['eventstore']['url'] + "/" + "buy" + "?timestamp="+ last_updated_format)
        buy_data = res_buy.json()
        buy_price = []
       
        print(buy_data)
        for item in buy_data:
            buy_price.append(float(item['price']))
        
        res_search = requests.get(app_config['eventstore']['url'] + "/" + "search" + "?timestamp="+ last_updated_format)
        search_data = res_search.json()
        search_price = []
        
        for item in search_data:
            search_price.append(float(item['price']))
        
        bs = Stats(
        len(buy_price),
        len(search_price),
        max(buy_price),
        max(search_price),
        min(buy_price),
        min(search_price),
        time
        )
        
        session.add(bs)
    session.commit()
    session.close()
    return NoContent, 201

def init_scheduler():
    """ initialize the scheduler to run periodically"""
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                'interval',
                seconds=app_config['scheduler']['period_sec']
                )
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)
