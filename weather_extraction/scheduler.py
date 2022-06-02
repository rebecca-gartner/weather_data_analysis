import schedule
import time
import datetime
import logging
import logging.config
import yaml
import pytz

with open("weather_extraction\config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

from weather_repository import load_weather_data_in_db
from weather_extraction import Weather_Extraction

weather_endpoint = "/weather"
tz = pytz.timezone("Europe/Berlin")

start_date = datetime.datetime(2022, 1, 1, 00, 00, 00).astimezone(
    pytz.timezone("Europe/Berlin")
)
start_date_utc = start_date.astimezone(pytz.utc)
end_date = datetime.datetime(2022, 4, 20, 20, 00, 00).astimezone(
    pytz.timezone("Europe/Berlin")
)
end_date_utc = end_date.astimezone(pytz.utc)
lat = "49.24"
lon = "8.41"
print(start_date_utc)
load_data = load_weather_data_in_db(
    weather_endpoint, start_date_utc, end_date_utc, lat, lon
)
load_data.insert_data()


# schedule.every().day.at("08:30").do(load.insert_data)

# while True:
#   schedule.run_pending()
#  time.sleep(1)
