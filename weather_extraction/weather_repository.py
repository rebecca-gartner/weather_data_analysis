from pymongo import MongoClient
from weather_extraction import Weather_Extraction
import datetime
import logging

logger = logging.getLogger(__name__)

weather_endpoint = "/weather"
# start_date = datetime.date.today()
# end_date = datetime.date.today()
# lat = "49.24"
# lon = "8.41"


class load_weather_data_in_db:
    """loads weather data which is extracted from
    BrightSky API into Weather DB
    """

    client = MongoClient(port=27017)
    db = client.weather_data

    def __init__(
        self,
        endpoint_name: str,
        start_date: datetime.date,
        end_date: datetime.date,
        lat: str,
        lon: str,
    ) -> None:
        self.endpoint_name = endpoint_name
        self.start_date = start_date
        self.end_date = end_date
        self.lat = lat
        self.lon = lon

    def insert_data(self) -> None:
        weather = Weather_Extraction(
            self.endpoint_name, self.start_date, self.end_date, self.lat, self.lon
        )
        extracted_data = weather.get_weather_for_timeseries()
        insertion_data = [
            {"insertion_date": datetime.datetime.now(), "data": sample}
            for sample in extracted_data
        ]
        print(insertion_data)

        result = self.db.reviews.insert_many(insertion_data)

        ids = result.inserted_ids

        logger.info("Data inserted into DB")

        return print(f"{ids} inserted in DB")
