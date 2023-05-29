import pandas as pd
import numpy as np
import json
import requests
import datetime
from shapely.geometry import mapping, shape
from shapely.prepared import prep
from shapely.geometry import Point

def load_df():
    ''' load, create and return dataframe object '''
    df_usgs = pd.read_csv('https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=1970-01-01&endtime=1970-12-31&minmagnitude=4')
    for year in range(1971, datetime.datetime.now().year + 1):
        df_usgs = df_usgs.append(pd.read_csv(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={year}-01-01&endtime={year}-12-31&minmagnitude=4'), ignore_index=True)
    return df_usgs

def create_countries_coord(data):
    ''' create countries coordinates dictionary '''
    countries = {}
    for feature in data["features"]:
        geom = feature["geometry"]
        country = feature["properties"]["ADMIN"]
        countries[country] = prep(shape(geom))
    return countries

def get_country(lon, lat, countries):
    ''' get country from coordinates '''
    point = Point(lon, lat)
    for country, geom in countries.items():
        if geom.contains(point):
            return country
    return ""

def handle_time(dateAndTime):
    ''' create year, month, day, date, time fields '''
    year = dateAndTime.apply(lambda x: x.year)
    month = dateAndTime.apply(lambda x: x.month)
    day = dateAndTime.apply(lambda x: x.day)
    time = dateAndTime.apply(lambda x: x.time())
    return year, month, day, time

def create_json(df1):
    ''' creatre json response '''
    df = df1.copy()
    df['database'] = "USGS Earthquake Program"
    df['time'] = pd.to_datetime(df['time'], format="%Y-%m-%dT%H:%M:%S.%fZ")
    df['openYear'], df['openMonth'], df['openDay'], df['openTime'] = handle_time(df['time'])
    df['openDate'] = df['time'].apply(lambda x: str(x)[:10])
    df['emergencyTypeEnum'] = 'EARTHQUAKE'
    df['depth'] = df['depth'].apply(lambda x: x * 1000 if not pd.isna(x) else "")
    df['magnitude'] = df['mag'].apply(lambda x: x if not pd.isna(x) else "")
    df['gap'] = df['gap'].apply(lambda x: x if not pd.isna(x) else "")
    df['dmin'] = df['dmin'].apply(lambda x: x if not pd.isna(x) else "")
    df['rms'] = df['rms'].apply(lambda x: x if not pd.isna(x) else "")
    df['locationArea'] = df['place'].apply(lambda x: x if not pd.isna(x) else "")
    df['horizontalError'] = df['horizontalError'].apply(lambda x: x * 1000 if not pd.isna(x) else "")
    df['depthError'] = df['depthError'].apply(lambda x: x * 1000 if not pd.isna(x) else "")
    df['magError'] = df['magError'].apply(lambda x: x if not pd.isna(x) else "")
    data = requests.get("https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson").json()
    countries = create_countries_coord(data)
    df['country'] = df[['longitude', 'latitude']].apply(lambda x: get_country(*x, countries=countries), axis=1)

    df = df[['database', 'emergencyTypeEnum', 'openYear', 'openMonth', 'openDay', 'openDate', 'openTime', 'latitude',\
             'longitude', 'depth', 'magnitude', 'gap', 'dmin', 'rms', 'locationArea', 'horizontalError',\
             'depthError', 'magError', 'country']]
    result = df.to_json(orient='records')
    response = json.loads(result)
    return response

def return_json():
    ''' return json response '''
    df = load_df()
    response = create_json(df)
    return response

    
