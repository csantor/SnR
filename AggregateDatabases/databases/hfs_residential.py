from . import hfs_forest
import pandas as pd
import json
import numpy as np
import os

def create_dataframe(list_of_files):
    ''' create pandas dataframe consisting of all the excel files '''
    last_df = pd.read_excel(list_of_files[0])
    last_df.rename(columns={'Σύνολο Πυροσβ. Πλοιαρίων': 'Σύνολο Πυροσβεστικών Πλοιαρίων', 'Αριθμός εμπλεκομένων   ανά τύπο ': 'Αριθμός εμπλεκομένων ανά τύπο ατυχήματος'}, inplace=True)
    for file in list_of_files[1:]:
        df = pd.read_excel(file)
        df.rename(columns={'Σύνολο Πυροσβ. Πλοιαρίων': 'Σύνολο Πυροσβεστικών Πλοιαρίων', 'Αριθμός εμπλεκομένων   ανά τύπο ': 'Αριθμός εμπλεκομένων ανά τύπο ατυχήματος'}, inplace=True)
        last_df = last_df.append(df, ignore_index=True)
    df = last_df[((last_df['Είδος Συμβάντος']=='ΠΥΡΚΑΓΙΑ') | (last_df['Είδος Συμβάντος']==' ΠΥΡΚΑΓΙΑ') | (last_df['Είδος Συμβάντος']=='ΔΕΛΤΙΟ ΠΥΡΚΑΓΙΑΣ')) & ((last_df['Χαρακτηρισμός Συμβάντος']=='ΜΙΚΡΗ') | (last_df['Χαρακτηρισμός Συμβάντος']=='ΜΕΣΑΙΑ') | (last_df['Χαρακτηρισμός Συμβάντος']=='ΜΕΓΑΛΗ'))]
    for file in list_of_files:
        os.remove(file)
    return df

def handle_float_values(x):
    ''' handle float and nan '''
    if pd.isna(x):
        return ""
    else:
        return int(x)


def map_severity(severity):
    ''' map severity '''
    severity_mapping = {
        'ΜΙΚΡΗ': 'MINOR',
        'ΜΕΣΑΙΑ': 'MEDIUM',
        'ΜΕΓΑΛΗ': 'MAJOR'
    }
    return severity.apply(lambda x: severity_mapping[x] if not pd.isna(x) else "")

def create_json(df):
    ''' create json response '''
    df['openYear'], df['openMonth'], df['openDay'], df['openDate'] = hfs_forest.create_open_date(df['Ημερ. Έναρξης Συμβάντος'])
    df['closeYear'], df['closeMonth'], df['closeDay'], df['closeDate'] = hfs_forest.create_open_date(df['Ημερ. Κατάσβεσης'])
    df['openTime'], df['closeTime'] = hfs_forest.create_time(df['Ώρα Έναρξης']), hfs_forest.create_time(df['Ώρα Κατάσβεσης'])
    df['fireFighters'] = df['Σύνολο Πυρ. Δυνάμεων (σε άνδρες και γυναίκες)'].apply(handle_float_values)
    df['fireTrucks'] = df['Σύνολο Πυρ. Οχημάτων'].apply(handle_float_values)
    df['fireShips'] = df['Σύνολο Πυροσβεστικών Πλοιαρίων'].apply(handle_float_values)
    df['country'] = 'Greece'
    df['emergencyTypeEnum'] = 'FIRE'
    df['locationType'] = 'Residential'
    df['region'] = hfs_forest.map_region(df['Νομός'])
    df['involvedPeopleNumber'] = df['Αριθμός εμπλεκομένων ανά τύπο ατυχήματος']
    df['injuredPeopleNumber'] = df['Τραυματίες'] + df['Εγκαύματα']
    df['casualties'] = df['Θάνατοι']
    df['severity'] = map_severity(df['Χαρακτηρισμός Συμβάντος'])
    df['database'] = 'Hellenic Fire Service (Residential)'
    result = df.loc[:, 'openYear':].to_json(orient='records')
    response = json.loads(result)
    return response

def return_json(list_of_files):
    ''' return json response '''
    df = create_dataframe(list_of_files)
    response = create_json(df)
    return response
