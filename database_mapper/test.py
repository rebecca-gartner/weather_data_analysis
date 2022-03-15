# import relevant modules
from pymongo import MongoClient
from random import randint
import pandas as pd
from datetime import datetime

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


sql_file = open("create_weather_table.sql", "r")
cursor.execute(sql_file.read())

weather_list = []

# print(col.find_one({"timestamp": "'2022-02-25T20:00:00+00:00'"}))
for x in col.find(
    {},
    {
        "weather.source_id": 1,
        "weather.timestamp": 1,
        "weather.temperature": 1,
        "weather.cloud_cover": 1,
        "weather.condition": 1,
        "weather.dew_point": 1,
        "weather.precipitation": 1,
        "weather.pressure_msl": 1,
        "weather.relative_humidity": 1,
        "weather.sunshine": 1,
        "weather.visibility": 1,
        "weather.wind_direction": 1,
        "weather.wind_speed": 1,
        "weather.wind_gust_direction": 1,
        "weather.wind_gust_speed": 1,
    },
):
    # print(x)
    weather_list = []
    weather_list.append(x)
    columns = list(weather_list[0]["weather"][0].keys())
    columns = "[{}]".format(", ".join(columns))
    # for i in range(0, len(weather_list["weather"])):
    # print(weather_list[0]["weather"][0])

    print(len(weather_list[0]["weather"]))
    if len(weather_list[0]["weather"]) < 4:
        for j in range(len(weather_list[0]["weather"])):

            weather_values_list = list(weather_list[0]["weather"][j].values())
            weather_values_list[0] = datetime.strptime(
                weather_values_list[0], "%Y-%m-%dT%H:%M:%S%z"
            )

            weather_values_tuple = tuple(weather_values_list)

            sql_file2 = open("insert_into_weather_table.sql", "r")
            cursor.execute(sql_file2.read(), weather_values_tuple)
    else:
        for j in range(0, 4):

            weather_values_list = list(weather_list[0]["weather"][j].values())
            weather_values_list[0] = datetime.strptime(
                weather_values_list[0], "%Y-%m-%dT%H:%M:%S%z"
            )

            weather_values_tuple = tuple(weather_values_list)

            sql_file2 = open("insert_into_weather_table.sql", "r")
            cursor.execute(sql_file2.read(), weather_values_tuple)


conn.commit()
conn.close()
