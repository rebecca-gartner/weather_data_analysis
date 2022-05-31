# Weather and Train Data Analysis

The goal of this project is to study the correlation between local train delays in Heidelberg and the weather. The weather data is extracted from [Bright Sky API](https://brightsky.dev/) which uses data from the Deutsche Wetterdienst. The train data is extracted from the RNV API, the API of the Rhein-Neckar-Verkehr GmbH. The API is used with the permission of the RNV, however, we are not associated with them in any way.

## Tasks

- extract weather data from [Bright Sky API](https://brightsky.dev/)
- insert weather data into [MongoDB (Community Server)](https://www.mongodb.com/try/download/community)
- load weather data stored in MongoDB in PostgreSQL
- extract information about train delays in Heidelberg from RNV API (https://opendata.rnv-online.de/dataset/data-hub-api-dokumentationen)
- derive meaningful insights from weather data

## Technologies

- [requests](https://docs.python-requests.org/en/latest/)
- [pymongo](https://pypi.org/project/pymongo/)
- object orientation
- [logging](https://realpython.com/python-logging/)
- [linting](https://code.visualstudio.com/docs/python/linting)
- [types](https://realpython.com/python-type-checking/)

## Setup

Install python dependencies using [pip](https://pypi.org/project/pip/):

```
pip install -r requirements.txt
```


## Formatting
We use black for formatting 
```
pip install black
```

To configure format-on-save go to Settings, search for Python formatting provider and select black. Then search for format-on-save and activate the checkbox. 

## Linting
We use Pylint for linting
```
pip install pylint
```

To enable linting in VS Code, type Ctr+Shift+P and type  "python select linter", then select pylint. 

## List of files needed to run this project
database.ini - for access to PostgreSQL
requirements.txt
config.py - to read out database.ini
Files that contain credentials to RNV API


## How to use this project
1. Apply for access to the RNV API. It might take a few days/weeks until one gets the credentials. (https://opendata.rnv-online.de/datahub-api). For the BrightSky API there are no credentials needed.
2. To extracts weather data from the BrightSky API, go to weather_extraction/scheduler.py and change longitute and latitude to the wanted values and change the start and end time to the wanted timeframe. Execute scheduler.py. The weather data is now inserted in MongoDB.
3. To load the weather data from MongoDB into a PostgreSQL table, go to database_mapper/mapper.py and change the date to a date that is within your weather data timeframe and execute mapper.py
4. To extract train data from the RNV API, go to trains/load_data.py and change start date, end date, hafasID and first_n to the wanted values. The hafasID is the ID of the train station from which data is extracted. first_n is number of journeys that should be extracted. The train data is loaded in a MongoDB collection.
5. To put the train data from the MongoDB collection into a PostgreSQL table, go to train_db_mapper/trainmapper.py and change the date to a date that is within your train data timeframe and execute trainmapper.py
6. Now the weather and train data is ready for analysis. An example for this is shown in traindelay_analysis.ipynb
