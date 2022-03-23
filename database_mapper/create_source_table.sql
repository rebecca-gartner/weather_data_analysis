CREATE  TABLE IF NOT EXISTS WEATHER_SOURCES(id int NOT NULL,
        dwd_station_id varchar(255),
        observation_type varchar(255),
        lat float,
        lon  float,
        height float,
        station_name varchar(255),
        wmo_station_id varchar(255),
        first_record timestamp,
        last_record timestamp,
        distance float
        );