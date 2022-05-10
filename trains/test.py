# import relevant modules

from train_delay_repository import load_train_data_in_db


# startTime = "2022-04-20T15:17:00Z"
hafasID = 4272
first_n = 2
hours1 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
hours2 = [x for x in range(10, 24)]
hours = hours1 + hours2
minutes1 = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"]
minutes2 = [x for x in range(10, 60)]
minutes = minutes1 + minutes2
from datetime import datetime
from dateutil import rrule

# dates
start_date = datetime(2022, 1, 12)
end_date = datetime(2022, 1, 15)

for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):

    for i in hours:
        for j in minutes:

            load_data = load_train_data_in_db(
                hafasID, f"{str(dt)[:10]}T{i}:{j}:00Z", first_n
            )
            load_data.insert_data()
