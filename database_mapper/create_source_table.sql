CREATE  TABLE IF NOT EXISTS WEATHER_SOURCES
    (id INT NOT NULL,
    dwd_station_id VARCHAR(255),
    observation_type VARCHAR(255),
    lat FLOAT,
    lon  FLOAT,
    height FLOAT,
    station_name VARCHAR(255),
    wmo_station_id VARCHAR(255),
    first_record timestamp,
    last_record timestamp,
    distance FLOAT
    )
;