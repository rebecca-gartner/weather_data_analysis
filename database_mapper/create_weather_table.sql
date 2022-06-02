CREATE  TABLE IF NOT EXISTS WEATHER_DETAILS4
    (timestamp TIMESTAMP,
    source_id INT NOT NULL,
    precipitation VARCHAR(255),
    pressure_msl FLOAT,
    sunshine  VARCHAR(255),
    temperature FLOAT,
    wind_direction FLOAT,
    wind_speed FLOAT,
    cloud_cover FLOAT,
    dew_point FLOAT,
    relative_humidity FLOAT,
    visibility FLOAT,
    wind_gust_direction FLOAT,
    wind_gust_speed FLOAT,
    condition VARCHAR(255),
    fallback_source_ids VARCHAR(255),
    icon VARCHAR(255)
    )
;