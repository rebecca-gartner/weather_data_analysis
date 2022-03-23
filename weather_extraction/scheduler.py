import schedule
import time
import datetime
import logging
import logging.config
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

from weather_repository import load_weather_data_in_db
from weather_extraction import Weather_Extraction

weather_endpoint = "/weather"
start_date = datetime.datetime(2022, 3, 20, 13, 00, 00)
# print(start_date)
end_date = datetime.datetime(2022, 3, 23, 12, 00, 00)
lat = "49.24"
lon = "8.41"

load_data = load_weather_data_in_db(weather_endpoint, start_date, end_date, lat, lon)
load_data.insert_data()

# schedule.every(5).seconds.do(load.insert_data)

# schedule.every().day.at("08:30").do(load.insert_data)

# while True:
#   schedule.run_pending()
#  time.sleep(1)
