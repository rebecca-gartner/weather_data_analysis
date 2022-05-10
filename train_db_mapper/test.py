from pymongo import MongoClient
from random import randint
import pandas as pd
from datetime import datetime
import dateutil.parser
import sys
import numpy as np
import psycopg2.extras as extras

import psycopg2

from config import config

params = config()

conn = psycopg2.connect(**params)
conn.autocommit = True
cursor = conn.cursor()


# connect to MongoDB and create Weather DB
client = MongoClient(port=27017)
db = client.train_data
col = db.traindelays


train_list = [
    {"stops": None},
    {"line": {"id": "26-26"}, "stops": []},
]
rebl = []
print(len(train_list[0]["stops"][0]["realtimeDeparture"]))
# rebl.append(train_list[0]["stops"][0]["realtimeDeparture"]["isoString"])
# print(rebl)
# rebl[0] = dateutil.parser.isoparse(rebl[0])
"""
line = []
hafasID = []
Station_name = []
for x in col.find({}, {"insertion_date": 1, "data": 1}):
    print(x)
    train_list.append(x)

# print(train_list)
"""
