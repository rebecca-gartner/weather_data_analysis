# import relevant modules
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


train_list = []

line = []
hafasID = []
Station_name = []
for x in col.find({}, {"data": 1}):
    train_list.append(x)

planned_departure = []
realtime_departure = []
stop_in_one_journey = []

for b in range(1, len(train_list)):
    print(b, len(train_list))

    if train_list[b]["data"]["station"]["journeys"] != None:
        print(train_list[b]["data"]["station"]["journeys"]["elements"])

        for x in range(len(train_list[b]["data"]["station"]["journeys"]["elements"])):
            # all stops in 1 journey
            for i in range(
                len(
                    train_list[b]["data"]["station"]["journeys"]["elements"][x]["stops"]
                )
            ):
                if (
                    train_list[b]["data"]["station"]["journeys"]["elements"][x][
                        "stops"
                    ][i]["plannedDeparture"]["isoString"]
                    != None
                    and train_list[b]["data"]["station"]["journeys"]["elements"][x][
                        "stops"
                    ][i]["realtimeDeparture"]["isoString"]
                    != None
                ):
                    planned_departure.append(
                        train_list[b]["data"]["station"]["journeys"]["elements"][x][
                            "stops"
                        ][i]["plannedDeparture"]["isoString"]
                    )
                    realtime_departure.append(
                        train_list[b]["data"]["station"]["journeys"]["elements"][x][
                            "stops"
                        ][i]["realtimeDeparture"]["isoString"]
                    )
                    line.append(
                        train_list[b]["data"]["station"]["journeys"]["elements"][x][
                            "line"
                        ]["id"]
                    )
                    hafasID.append(train_list[b]["data"]["station"]["hafasID"])
                    Station_name.append(train_list[b]["data"]["station"]["longName"])
                    stop_in_one_journey.append(i)


timediff = []

if len(planned_departure) != len(realtime_departure):
    print("Error: None Value as depature time")
    sys.exit()
for j in range(len(planned_departure)):
    realtime_departure[j] = dateutil.parser.isoparse(realtime_departure[j])
    planned_departure[j] = dateutil.parser.isoparse(planned_departure[j])
    timediff.append((realtime_departure[j] - planned_departure[j]))

data = {
    "hafasID": hafasID,
    "Stationname": Station_name,
    "Line": line,
    "stop_in_one_journey": stop_in_one_journey,
    "planned_departure": planned_departure,
    "realtime_departure": realtime_departure,
    "delay": timediff,
}


# Create DataFrame
df = pd.DataFrame(data)
print(df)
df["planned_departure"] = df["planned_departure"].astype(str)
df["realtime_departure"] = df["realtime_departure"].astype(str)

df = df[df["planned_departure"].str.contains("2022", regex=True)]
df = df[df["realtime_departure"].str.contains("2022", regex=True)]
df = df.drop_duplicates()
print(df)


sql = """CREATE TABLE IF NOT EXISTS traindelays(hafasID int ,
Stationname char(200) ,line char(20),stop_in_one_journey int, planned_departure char(30), realtime_departure char(30), delay interval);"""

cursor.execute(sql)


def execute_values(conn, df, table):

    tuples = [tuple(x) for x in df.to_numpy()]

    cols = ",".join(list(df.columns))

    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("execute_values() done")
    cursor.close()


# using the function defined
execute_values(conn, df, "traindelays")


conn.commit()
conn.close()
