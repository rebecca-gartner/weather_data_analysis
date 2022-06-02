# import relevant modules
import sys
from datetime import datetime
import os
from pymongo import MongoClient
import pandas as pd
import dateutil.parser
import psycopg2.extras as extras
import psycopg2
from config import config
from asyncio.log import logger


PARAMS = config()
DATE = 2022


def main() -> None:

    with psycopg2.connect(**PARAMS) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True

            # connect to MongoDB and create Train DB
            client = MongoClient(port=os.environ.get("PORT"))
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

                if train_list[b]["data"]["station"]["journeys"] != None:

                    for b in range(
                        len(train_list[b]["data"]["station"]["journeys"]["elements"])
                    ):
                        # all stops in 1 journey
                        for i in range(
                            len(
                                train_list[b]["data"]["station"]["journeys"][
                                    "elements"
                                ][x]["stops"]
                            )
                        ):
                            if (
                                train_list[b]["data"]["station"]["journeys"][
                                    "elements"
                                ][x]["stops"][i]["plannedDeparture"]["isoString"]
                                != None
                                and train_list[b]["data"]["station"]["journeys"][
                                    "elements"
                                ][x]["stops"][i]["realtimeDeparture"]["isoString"]
                                != None
                            ):
                                planned_departure.append(
                                    train_list[b]["data"]["station"]["journeys"][
                                        "elements"
                                    ][x]["stops"][i]["plannedDeparture"]["isoString"]
                                )
                                realtime_departure.append(
                                    train_list[b]["data"]["station"]["journeys"][
                                        "elements"
                                    ][x]["stops"][i]["realtimeDeparture"]["isoString"]
                                )
                                line.append(
                                    train_list[b]["data"]["station"]["journeys"][
                                        "elements"
                                    ][x]["line"]["id"]
                                )
                                hafasID.append(
                                    train_list[b]["data"]["station"]["hafasID"]
                                )
                                Station_name.append(
                                    train_list[b]["data"]["station"]["longName"]
                                )
                                stop_in_one_journey.append(i)

            timediff = []

            if len(planned_departure) != len(realtime_departure):
                logger.error("Error: None Value as depature time")
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
            df["planned_departure"] = df["planned_departure"].astype(str)
            df["realtime_departure"] = df["realtime_departure"].astype(str)

            df = df[df["planned_departure"].str.contains(f"{DATE}", regex=True)]
            df = df[df["realtime_departure"].str.contains(f"{DATE}", regex=True)]
            df = df.drop_duplicates()

            # create PostgreSQL table
            sql = """CREATE TABLE IF NOT EXISTS traindelays3
                (hafasID INT ,
                Stationname CHAR(200) ,
                line CHAR(20),
                stop_in_one_journey INT, 
                planned_departure CHAR(30), 
                realtime_departure CHAR(30), 
                delay INTERVAL)
                ;"""

            # load values from DataFrame in PostgreSQL table
            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ",".join(list(df.columns))

            # SQL query to execute
            query = "INSERT INTO %s(%s) VALUES %%s" % ("traindelays3", cols)

            try:
                extras.execute_values(cursor, query, tuples)

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error: %s" % error)
                conn.rollback()


if __name__ == "__main__":
    main()
