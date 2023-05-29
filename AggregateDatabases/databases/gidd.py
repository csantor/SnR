import pandas as pd
import json

def clean_df(df):
    ''' drop first column containing invalid headers '''
    df.drop([0], inplace=True)
    return df

def handle_date(date):
    ''' get month, day from date '''
    month = date.apply(lambda x: x.month)
    day = date.apply(lambda x: x.day)
    return month, day

def map_emergency(emergency):
    ''' map emergency types '''
    emergency_mapping = {
        'Flood': 'FLOOD',
        'Extreme temperature': "",
        'Earthquake': "EARTHQUAKE",
        'Wet mass movement': "FLOOD",
        'Dry mass movement': "LANDSLIDE",
        'Storm': "STORM",
        'Drought': "",
        'Volcanic eruption': "VOLCANO",
        'Wildfire': "FIRE",
        'Mass movement': "LANDSLIDE",
        'Volcanic activity': "VOLCANO",
        'Wet Mass movement': "FLOOD",
        'Severe winter condition': "AVALANCHE",
        'Wet Mass Movement': "FLOOD"
    }
    return emergency.apply(lambda x: emergency_mapping[x] if not pd.isna(x) else "")

def create_json(df):
    ''' create json response '''
    df['database'] = 'Global Internal Displacement Database'
    df['country'] = df['Name'].apply(lambda x: x if not pd.isna(x) else "")
    df['openYear'] = df['Year']
    df['date'] = pd.to_datetime(df['Start Date'])
    df['openMonth'], df['openDay'] = handle_date(df['date'])
    df['openDate'] = df['Start Date']
    df['description'] = df['Event Name'].apply(lambda x: x if not pd.isna(x) else "")
    df['emergencyTypeEnum'] = map_emergency(df['Hazard Type'])
    df['evacuatedPeopleNumber'] = df['New Displacements'].apply(lambda x: int(x) if not pd.isna(x) else "")
    df = df[['database', 'country', 'openYear', 'openMonth', 'openDay', 'openDate', 'description', 'emergencyTypeEnum', 'evacuatedPeopleNumber']]
    result = df.loc[:, 'database':].to_json(orient='records')
    response = json.loads(result)
    return response

def return_json(df):
    ''' return json response '''
    df = clean_df(df)
    response = create_json(df)
    return response