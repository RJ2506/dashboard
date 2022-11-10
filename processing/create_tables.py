import sqlite3
conn = sqlite3.connect('stats.sqlite')
c = conn.cursor()
c.execute('''
    CREATE TABLE stats
    (id INTEGER PRIMARY KEY ASC, 
    num_buy_readings INTEGER NOT NULL,
    num_search_readings INTEGER NOT NULL,
    max_buy_reading INTEGER,
    max_search_reading INTEGER,
    min_buy_reading INTEGER,
    min_search_reading INTEGER,
    last_updated VARCHAR(100) NOT NULL)
    ''')

conn.commit()
conn.close()