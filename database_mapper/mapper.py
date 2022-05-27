# import relevant modules
from asyncio.log import logger
from datetime import datetime
from pymongo import MongoClient
import pytz

import psycopg2
from config import config

date = 2022


def main(Date):
    """
    extracts weather data from MongoDB and inserts it into a PostreSQL table

    parameter:
    date: date for which weather data exists in MongoDB
    """
    # connect to MongoDB and create Weather DB
    client = MongoClient(port=27017)
    db = client.weather_data
    col = db.reviews

    params = config()

    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cursor = conn.cursor()

    # creates a PostgreSQL table that contains the weather data
    with open(
        "database_mapper\create_weather_table.sql",
        "r",
    ) as sql_file:
        cursor.execute(sql_file.read())

    # creates a PostgreSQL table that contains the sources of the weather data
    with open(
        "database_mapper\create_source_table.sql",
        "r",
    ) as sql_file:
        cursor.execute(sql_file.read())

    # in the source table every source should only be listed once.
    # Therefore the distinct source ids are  put in the id_list
    with open(
        "database_mapper\check_source_id.sql",
        "r",
    ) as sql_file:
        cursor.execute(sql_file.read())

    ids = cursor.fetchall()
    id_list = []
    if len(ids) > 0:
        for i in range(len(ids[0])):
            id_list.append(ids[0][i])

    # all weather data that has the given timestamp in
    # its collection is added to the weather_list
    weather_list = []
    try:
        x = col.find_one(
            {"data.weather.timestamp": {"$regex": f".*{date}.*"}}
        )  # in UTC time
    except:
        logger.info("no matching entry found in MongoDB")

    weather_list.append(x)

    columns = list(weather_list[0]["data"]["weather"][0].keys())

    columns = "[{}]".format(", ".join(columns))

    # the weather data gets extracted from the weather_list (which
    # also contains some unneccessary data)
    for j in range(len(weather_list[0]["data"]["weather"])):

        weather_values_list = list(weather_list[0]["data"]["weather"][j].values())
        # changes timezone to European time
        weather_values_list[0] = datetime.strptime(
            weather_values_list[0], "%Y-%m-%dT%H:%M:%S%z"
        )
        weather_values_list[0] = weather_values_list[0].astimezone(
            pytz.timezone("Europe/Berlin")
        )

        # the BrightSky API also gives us weather information from
        # the fallback source id. However, this is usually not
        # relevant and therefore all the information is put into
        # a string and added as one column to the weather table
        weather_values_list[15] = str(weather_values_list[15])

        # weather data gets inserted in weather table
        weather_values_tuple = tuple(weather_values_list)
        with open(
            "database_mapper\insert_into_weather_table.sql",
            "r",
        ) as sql_file:
            cursor.execute(sql_file.read(), weather_values_tuple)

    # all distinct sources get inserted in the source table
    for j in range(len(weather_list[0]["data"]["sources"])):
        weather_source_tuple = tuple(
            list(weather_list[0]["data"]["sources"][j].values())
        )

        if weather_source_tuple[0] not in id_list:
            with open(
                "database_mapper\insert_into_source_table.sql",
                "r",
            ) as sql_file:
                cursor.execute(sql_file.read(), weather_source_tuple)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main(date)
