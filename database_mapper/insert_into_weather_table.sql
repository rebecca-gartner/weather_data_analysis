insert into WEATHER_DETAILS4(

    timestamp ,
    source_id ,
    precipitation,
    pressure_msl ,
    sunshine  ,
    temperature ,
    wind_direction ,
    wind_speed ,
    cloud_cover ,
    dew_point ,
    relative_humidity ,
    visibility ,
    wind_gust_direction ,
    wind_gust_speed,
    condition ,
    fallback_source_ids,
    icon) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);