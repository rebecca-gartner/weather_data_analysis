# import relevant modules
from pymongo import MongoClient
from random import randint
import requests
from datetime import date, timedelta


# define needed functions
def get_url_by_endpoint_name(endpoint_name):
    system_url = "https://api.brightsky.dev"
    return system_url + endpoint_name


def get_weather_for_timeseries(start_date, end_date, lat, lon):
    """sends multiple GET requests to Bright Sky API for dates within start_date and end_date and returns list of JSON objects

    -------------
    Parameter:
    - start_date: First day in time series. Format: date(year, month, day)
    - end_date: Last day in time series. Format: date(year, month, day)
    - lat: latitude of place where weather information is wanted. String
    - lon: longitute of place where weather information is wanted. String

    """
    day_delta = end_date - start_date

    for i in range(day_delta.days + 1):
        day = start_date + timedelta(days=i)
        # print(day)
        dicto = {"date": f"{day}", "lat": lat, "lon": lon}
        r = requests.get(get_url_by_endpoint_name(weather_endpoint), params=dicto)
        day_weather = r.json()
        timeseries_weather.append(day_weather)

    return timeseries_weather


# connect to MongoDB and create Weather DB
client = MongoClient(port=27017)
db = client.weather_data

# declare variables
weather_endpoint = "/weather"
timeseries_weather = []
start_date = date(2022, 1, 1)
end_date = date(2022, 1, 7)
lat = "49.24"
lon = "8.41"

# get weather data from API
get_weather_for_timeseries(start_date, end_date, lat, lon)

# insert data into DB
if start_date != end_date:
    result = db.reviews.insert_many(timeseries_weather)
    print(result.inserted_ids)
else:
    result = db.reviews.insert_one(timeseries_weather)
    print(result.inserted_ids)

# fivestarcount = next(db.weather_data.find({}))
# print(fivestarcount)
print(get_weather_for_timeseries(start_date, end_date, lat, lon))
