# import relevant modules
import requests
from datetime import timedelta, date
import logging
import typing

logger = logging.getLogger(__name__)


class Weather_Extraction:
    """sends multiple GET requests to Bright Sky API for dates within start_date
    and end_date and returns list of JSON objects

    -------------
    Parameter:
    - start_date: First day in time series. Format: date(year, month, day)
    - end_date: Last day in time series. Format: date(year, month, day)
    - lat: latitude of place where weather information is wanted. String
    - lon: longitute of place where weather information is wanted. String

    """

    system_url = "https://api.brightsky.dev"
    timeseries_weather: typing.List[dict] = []

    def __init__(
        self, endpoint_name: str, start_date: date, end_date: date, lat: str, lon: str
    ) -> None:
        self.endpoint_name = endpoint_name
        self.start_date = start_date
        self.end_date = end_date
        self.lat = lat
        self.lon = lon

    def get_weather_for_timeseries(self) -> typing.List[dict]:
        day_delta = self.end_date - self.start_date

        for i in range(day_delta.days + 1):
            day = self.start_date + timedelta(days=i)
            dicto = {"date": f"{day}", "lat": self.lat, "lon": self.lon}
            r = requests.get(self.system_url + self.endpoint_name, params=dicto)
            day_weather = r.json()
            self.timeseries_weather.append(day_weather)

        logging.info("Weather data extracted")

        return self.timeseries_weather
