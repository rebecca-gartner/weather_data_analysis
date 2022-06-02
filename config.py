from configparser import ConfigParser
import sys

# adding Folder_2 to the system path
sys.path.insert(
    0,
    "/Users/becci/OneDrive/Documents/Gap Year/weather_and_trains/weather_data_analysis",
)


def config(filename="database.ini", section="postgresql") -> dict:
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            f"Section {section} not found in the {filename} file",
            print(filename),
        )

    return db
