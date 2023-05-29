import pandas as pd
import json
import datetime

def load_df():
    ''' load dataframe from source '''
    df = pd.read_csv("https://data.nasa.gov/api/views/dd9e-wu2v/rows.csv")
    return df

def create_date(date):
    ''' create year, day, month, date fields '''
    year = date.apply(lambda x: int(x[6:10]))
    day = date.apply(lambda x: int(x[3:5]))
    month = date.apply(lambda x: int(x[:2]))
    final_date = date.apply(lambda x: x[6:10] + "-" + x[:2] + "-" + x[3:5])
    return year, month, day, final_date
    
def transform_am_pm(time):
    ''' transform time from am/pm to 24h '''
    if time[:2] == "12" and time[-2:] == "AM":
        return "00" + time[2:-3]
    elif time[-2:] == "AM":
        return time[:-3]
    elif time[:2] == "12" and time[-2:] == "PM":
        return "12" + time[2:-3]
    else:
        return str(int(time[:2]) + 12) + time[2:-3]

def create_time(date):
    ''' create time as datetime.datetime.time object '''
    final_time = date.apply(lambda x: datetime.datetime.strptime(transform_am_pm(x[11:]), '%H:%M:%S').time())
    return final_time

def map_cause(trigger):
    '''map triggers'''
    trigger_mapping = {
        'unknown': '',
        'no_apparent_trigger': '',
        'other': ''
    }
    if trigger in trigger_mapping:
        return trigger_mapping[trigger]
    elif pd.isna(trigger):
        return ''
    else:
        return trigger
    
def map_severity(landslide_size):
    ''' map severity '''
    severity_mapping = {
        'small': 'MINOR',
        'medium': 'MEDIUM',
        'large': 'MAJOR',
        'very_large': 'CRITICAL',
        'catastrophic': 'CRITICAL',
        'unknown': ''
    }
    if pd.isna(landslide_size):
        return ''
    else:
        return severity_mapping[landslide_size]
    
def map_location_type(landslide_setting):
    ''' map location types '''
    location_type_mapping = {
        'mine': 'Industrial',
        'unknown': '',
        'above_road': 'Residential',
        'urban': 'Residential',
        'natural_slope': 'Non-residential',
        'engineered_slope': 'Man-made open space',
        'below_road': 'Residential',
        'above_river': 'Non-residential',
        'retaining_wall': 'Infrastructure',
        'other': '',
        'above_coast': 'Non-residential',
        'bluff': 'Non-residential',
        'burned_area': 'Non-residential',
        'deforested_slope': 'Non-residential'
    }
    if pd.isna(landslide_setting):
        return ''
    else:
        return location_type_mapping[landslide_setting]

def create_json(df):
    ''' create json response '''
    df['database'] = 'Global Landslide Catalog'
    df['reportedDate'] = df['submitted_date'].apply(lambda x: str(datetime.datetime.strptime(x[:10], '%m/%d/%Y').date()) if not pd.isna(x) else '')
    df['title'] = df['event_title']
    df['description'] = df['event_description'].apply(lambda x: x if not pd.isna(x) else '')
    df['cause'] = df['landslide_trigger'].apply(map_cause)
    df['severity'] = df['landslide_size'].apply(map_severity)
    df['openYear'], df['openMonth'], df['openDay'], df['openDate'] = create_date(df['event_date'])
    df['openTime'] = create_time((df['event_date']))
    df['country'] = df['country_name'].apply(lambda x: x if not pd.isna(x) else '')
    df['locationType'] = df['landslide_setting'].apply(map_location_type)
    df['casualties'] = df['fatality_count'].apply(lambda x: int(x) if not pd.isna(x) else 0)
    df['injuredPeopleNumber'] = df['injury_count'].apply(lambda x: int(x) if not pd.isna(x) else 0)
    df['emergencyTypeEnum'] = 'LANDSLIDE'
    df = pd.concat([df.loc[:, 'database':], df[['latitude', 'longitude']]], axis=1)
    result = df.to_json(orient='records')
    response = json.loads(result)
    return response

def return_json():
    ''' return json response '''
    df = load_df()
    response = create_json(df)
    return response