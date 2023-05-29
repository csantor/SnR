import pandas as pd
import requests
import json
import datetime
import unicodedata
import pycountry
import datetime

def map_event_type(event_type):
    ''' map events to emergency'''
    event_mapping = {
        'FL': 'FLOOD',
        'EQ': 'EARTHQUAKE',
        'TC': 'STORM',
        'VO': 'VOLCANO'
    }
    return event_type.apply(lambda x: event_mapping[x] if not (pd.isna(x) or x == 'DR') else "")

def map_iso3(iso3):
    ''' map iso3 to country names'''
    if pd.isna(iso3) or iso3 == '   ' or iso3 == '':
        return ''
    else:
        if pd.isna(pycountry.countries.get(alpha_3=iso3)):
            return ''
        else:
            return pycountry.countries.get(alpha_3=iso3).name

def get_country(row):
    ''' create country column from iso3 or location area information '''
    if row['iso3'] != '':
        return row['iso3']
    else:
        if ',' in row['locationarea']:
            return ''
        else:
            return row['locationarea']
        
def handle_date(date):
    ''' create year, month, day, time fields '''
    year = date.apply(lambda x: x.year)
    month = date.apply(lambda x: x.month)
    day = date.apply(lambda x: x.day)
    time = date.apply(lambda x: x.time())
    return year, month, day, time

def create_json(df):
    ''' create json response '''
    df['emergencyTypeEnum'] = map_event_type(df['eventtype'])
    df['fromdate'] = df['fromdate'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    df['todate'] = df['todate'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S'))
    df['openYear'], df['openMonth'], df['openDay'], df['openTime'] = handle_date(df['fromdate'])
    df['openDate'] = df['fromdate'].apply(lambda x: str(x))
    df['closeYear'], df['closeMonth'], df['closeDay'], df['closeTime'] = handle_date(df['todate'])
    df['closeDate'] = df['todate'].apply(lambda x: str(x))
    df['iso3'] = df.iso3.apply(map_iso3)
    df['locationarea'] = df['locationarea'].apply(lambda x: unicodedata.normalize("NFKD", x).strip())
    df['country'] = df.apply(get_country, axis=1)
    df['country'] = df['country'].apply(lambda x: 'United States of America' if x == 'USA' or x == 'United States' else x)
    df.country[df.country == 'Virgin IslandsU.S.GuadeloupePuerto RicoDominicaTurks and Caicos IslandsDominican RepublicMartiniqueAntigua and BarbudaMontserratSaint Kitts and NevisAnguillaBritish'] = ''
    df.country[df.country == '-1'] = ''
    df.alertlevel = df.alertlevel.apply(lambda x: x.upper())
    df.episodealertlevel = df.episodealertlevel.apply(lambda x: x.upper())
    df['magnitude'] = df['severitytext'].apply(lambda x: float(''.join(c for c in x[8:14] if c.isdigit() or c == '.')) if 'Magnitude' in x else '')
    df['depth'] = df['severitytext'].apply(lambda x: float(''.join(c for c in x[-8:] if c.isdigit() or c == '.')) * 1000 if 'Depth' in x else '')
    df = df[['latitude', 'longitude', 'emergencyTypeEnum', 'description', 'alertlevel',
       'alertscore', 'episodealertlevel', 'episodealertscore', 'locationarea', 'severitytext', 'openYear', 'openMonth', 'openDay',
       'openTime', 'openDate', 'closeYear', 'closeMonth', 'closeDay', 'closeTime', 'closeDate', 'country', 'magnitude', 'depth']]
    result = df.to_json(orient='records')
    response = json.loads(result)
    return response

def return_json(df):
    ''' return json response '''
    response = create_json(df)
    return response
