# import relevant modules
from pymongo import MongoClient
from random import randint
import pandas as pd
from datetime import datetime
import pytz

import psycopg2
from config import config


# connect to MongoDB and create Weather DB
client = MongoClient(port=27017)
db = client.weather_data
col = db.reviews

params = config()

conn = psycopg2.connect(**params)
conn.autocommit = True
cursor = conn.cursor()


sql_file = open("database_mapper\create_weather_table.sql", "r")
cursor.execute(sql_file.read())

sql_file = open("database_mapper\create_source_table.sql", "r")
cursor.execute(sql_file.read())

sql_file = open("database_mapper\check_source_id.sql", "r")
get_ids = cursor.execute(sql_file.read())
ids = cursor.fetchall()
id_list = []
if len(ids) > 0:
    for i in range(len(ids[0])):
        id_list.append(ids[0][i])


weather_list = []

x = col.find_one(
    {"data.weather.timestamp": {"$regex": ".*2022-01-01T13.*"}}
)  # in UTC time

weather_list.append(x)

columns = list(weather_list[0]["data"]["weather"][0].keys())

columns = "[{}]".format(", ".join(columns))


for j in range(len(weather_list[0]["data"]["weather"])):

    weather_values_list = list(weather_list[0]["data"]["weather"][j].values())
    weather_values_list[0] = datetime.strptime(
        weather_values_list[0], "%Y-%m-%dT%H:%M:%S%z"
    )
    weather_values_list[0] = weather_values_list[0].astimezone(
        pytz.timezone("Europe/Berlin")
    )

    weather_values_list[15] = str(weather_values_list[15])

    weather_values_tuple = tuple(weather_values_list)
    sql_file2 = open("database_mapper\insert_into_weather_table.sql", "r")
    cursor.execute(sql_file2.read(), weather_values_tuple)

for j in range(len(weather_list[0]["data"]["sources"])):
    weather_source_tuple = tuple(list(weather_list[0]["data"]["sources"][j].values()))

    if weather_source_tuple[0] not in id_list:
        sql_file2 = open("database_mapper\insert_into_source_table.sql", "r")
        cursor.execute(sql_file2.read(), weather_source_tuple)


conn.commit()
conn.close()
