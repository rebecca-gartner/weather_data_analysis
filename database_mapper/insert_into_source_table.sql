insert into WEATHER_SOURCES(

    id ,
    dwd_station_id ,
    observation_type,
    lat ,
    lon  ,
    height ,
    station_name ,
    wmo_station_id ,
    first_record ,
    last_record ,
    distance) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);