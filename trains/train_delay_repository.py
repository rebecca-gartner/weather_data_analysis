from pymongo import MongoClient
from train_delay_extraction import Train_Delay_Extraction
import logging

logger = logging.getLogger(__name__)


class load_train_data_in_db:
    """loads train data which is extracted from
    RNV API into Train DB
    """

    client = MongoClient(port=27017)
    db = client.train_data

    def __init__(self, hafasID: int, startTime: str, first_n: int) -> None:
        self.hafasID = hafasID
        self.startTime = startTime
        self.first_n = first_n

    def insert_data(self) -> None:
        delays = Train_Delay_Extraction(self.hafasID, self.startTime, self.first_n)
        extracted_data = delays.get_departure_times()

        result = self.db.traindelays.insert_one(extracted_data)

        ids = result.inserted_id

        logger.info("Data inserted into DB")

        return print(f"{ids} inserted in DB")


startTime = "2022-03-26T11:17:00Z"
hafasID = 4272
first_n = 5

load_data = load_train_data_in_db(hafasID, startTime, first_n)
load_data.insert_data()
