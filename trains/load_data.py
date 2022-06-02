# import relevant modules
from train_delay_repository import load_train_data_in_db
from datetime import datetime
from dateutil import rrule


hours1 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
hours2 = list(range(10, 24))
hours = hours1 + hours2
minutes1 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
minutes2 = list(range(10, 60))
minutes = minutes1 + minutes2


# dates
START_DATE = datetime(2022, 1, 12)
END_DATE = datetime(2022, 1, 15)
HAFAS_ID = 4272
FIRST_N = 2


def main(start_date, end_date, hafasID, first_n) -> None:
    """
    loads train delays data in MongoDB for every minute between START_DATE and
    END_DATE for a given hafasID and number of journeys

    parameters:
    - START_DATE: start time of the journey, format datetime
    - END_DATE: end time of the journey, format datetime
    - hafasID: hafasID of the train station
    - first_n: number of journeys that should be extracted. int
    """
    for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):

        for i in hours:
            for j in minutes:

                load_data = load_train_data_in_db(
                    hafasID, f"{str(dt)[:10]}T{i}:{j}:00Z", first_n
                )
                load_data.insert_data()


if __name__ == "__main__":
    main(START_DATE, END_DATE, HAFAS_ID, FIRST_N)
