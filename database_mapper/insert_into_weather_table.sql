insert into WEATHER_DETAILS3(

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
    condition ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);