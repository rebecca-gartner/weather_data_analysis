# Weather Data Analysis

## Tasks

- extract weather data from [Bright Sky API](https://brightsky.dev/)
- insert weather data into [MongoDB (Community Server)](https://www.mongodb.com/try/download/community)
- load weather data stored in MongoDB in PostgreSQL
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

(`requirements.txt` still needs to be added)

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

{'hafasID': '1160', 'globalID': 'de:08221:1160', 'longName': 'Heidelberg Hauptbahnhof'}, 
{'hafasID': '1214', 'globalID': 'de:08221:1214', 'longName': 'Heidelberg Hauptbahnhof West'}, {'hafasID': '1144', 'globalID': 'de:08221:1144', 'longName': 'Betriebshof'},
 {'hafasID': '4272', 'globalID': 'de:08221:4272', 'longName': 'Heidelberg Hauptbahnhof Süd'},

