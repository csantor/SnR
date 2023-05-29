import pandas as pd
import datetime
import json
import numpy as np
import os


def create_dataframe(list_of_files):
    ''' create pandas dataframe consisting of all the excel files and sheets '''
    df1 = pd.read_excel(list_of_files[0], sheet_name=0, skiprows=1)
    df1.rename(columns={'Σκουπιδότοποι': 'Σκουπι-δότοποι', 'ΜΗΧΑΝΗΜΑΤΑ': 'ΜΗΧΑΝΗ-ΜΑΤΑ'}, inplace=True)
    for sheet in range(1, 13):
        df2 = pd.read_excel(list_of_files[0], sheet_name=sheet, skiprows=1)
        df2.rename(columns={'Σκουπιδότοποι': 'Σκουπι-δότοποι', 'ΜΗΧΑΝΗΜΑΤΑ': 'ΜΗΧΑΝΗ-ΜΑΤΑ'}, inplace=True)
        df1 = df1.append(df2, ignore_index=True)
    for file in list_of_files[1:]:
        if file == 'Dasikes_Pyrkagies_2014.xlsx':
            df2 = pd.read_excel(file)
        else:
            df2 = pd.read_excel(file, skiprows=1)
        df2.rename(columns={'Σκουπιδότοποι': 'Σκουπι-δότοποι', 'ΜΗΧΑΝΗΜΑΤΑ': 'ΜΗΧΑΝΗ-ΜΑΤΑ'}, inplace=True)
        df1 = df1.append(df2, ignore_index=True)
    for file in list_of_files:
        os.remove(file)
    return df1

def check_time(x):
    ''' handle time strings '''
    if isinstance(x, str):
        return datetime.datetime.strptime(x, '%H:%M').time()
    elif isinstance(x, datetime.time):
        return x
    else:
        return ""

def create_open_date(date):
    ''' create open date fields (year, month, day) and return date as a string as well '''
    year = date.apply(lambda x: x.year if type(x) != pd._libs.tslibs.nattype.NaTType else "")
    month = date.apply(lambda x: x.month if type(x) != pd._libs.tslibs.nattype.NaTType else "")
    day = date.apply(lambda x: x.day if type(x) != pd._libs.tslibs.nattype.NaTType else "")
    final_date = date.apply(lambda x: str(x).split(' ')[0] if type(x) != pd._libs.tslibs.nattype.NaTType else "")
    return year, month, day, final_date


def create_close_date(date):
    ''' create close date fields (year, month, day) and return date as a string as well '''
    year = date.apply(lambda x: x.year if not pd.isna(x) and not isinstance(x, str) else "")
    month = date.apply(lambda x: x.month if not pd.isna(x) and not isinstance(x, str) else "")
    day = date.apply(lambda x: x.day if not pd.isna(x) and not isinstance(x, str) else "")
    final_date = date.apply(lambda x: str(x.date()) if not pd.isna(x) and not isinstance(x, str) else "")
    return year, month, day, final_date

def create_time(time):
    ''' create time field '''
    final_time = time.apply(check_time)
    return final_time

def sum_columns(df):
    ''' sum columns and handle na '''
    new_df = df[df.columns[0]].apply(lambda x: x if not pd.isna(x) else 0)
    for column in df.columns[1:]:
        new_df += df[column].apply(lambda x: x if not pd.isna(x) else 0)
    return new_df

def map_region(region):
    ''' map hfs "Νομός" to english names '''
    region_mapping = {
    'ΑΤΤΙΚΗΣ': 'Attica',
    'ΡΟΔΟΠΗΣ': 'Rhodope',
    'ΚΑΒΑΛΑΣ': 'Kavala',
    'ΔΡΑΜΑΣ': 'Drama',
    'ΞΑΝΘΗΣ': 'Xanthi',
    'ΕΒΡΟΥ': 'Evros',
    'ΘΕΣΣΑΛΟΝΙΚΗΣ': 'Thessaloniki',
    'ΣΕΡΡΩΝ': 'Serres',
    'ΧΑΛΚΙΔΙΚΗΣ': 'Chalkidiki',
    'ΚΙΛΚΙΣ': 'Kilkis',
    'ΠΕΛΛΑΣ': 'Pella',
    'ΗΜΑΘΙΑΣ': 'Imathia',
    'ΠΙΕΡΙΑΣ': 'Pieria',
    'ΚΟΖΑΝΗΣ': 'Kozani',
    'ΦΛΩΡΙΝΑΣ': 'Florina',
    'ΚΑΣΤΟΡΙΑΣ': 'Kastoria',
    'ΓΡΕΒΕΝΩΝ': 'Grevena',
    'ΙΩΑΝΝΙΝΩΝ': 'Ioannina',
    'ΘΕΣΠΡΩΤΙΑΣ': 'Thesprotia',
    'ΑΡΤΑΣ': 'Arta',
    'ΠΡΕΒΕΖΗΣ': 'Preveza',
    'ΛΑΡΙΣΑΣ': 'Larissa',
    'ΜΑΓΝΗΣΙΑΣ': 'Magnesia',
    'ΤΡΙΚΑΛΩΝ': 'Trikala',
    'ΚΑΡΔΙΤΣΑΣ': 'Karditsa',
    'ΑΧΑΙΑΣ': 'Achaea',
    'ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑΣ': 'Aetolia-Acarnania',
    'ΗΛΕΙΑΣ': 'Elis',
    'ΑΡΚΑΔΙΑΣ': 'Arcadia',
    'ΜΕΣΣΗΝΙΑΣ': 'Messenia',
    'ΛΑΚΩΝΙΑΣ': 'Laconia',
    'ΑΡΓΟΛΙΔΟΣ': 'Argolis',
    'ΚΟΡΙΝΘΙΑΣ': 'Corinthia',
    'ΦΘΙΩΤΙΔΑΣ': 'Phtiotis',
    'ΕΥΡΥΤΑΝΙΑΣ': 'Evrytania',
    'ΦΩΚΙΔΟΣ': 'Phocis',
    'ΒΟΙΩΤΙΑΣ': 'Boeotia',
    'ΕΥΒΟΙΑΣ': 'Euboea',
    'ΚΥΚΛΑΔΩΝ': 'Cyclades',
    'ΔΩΔΕΚΑΝΗΣΩΝ': 'Dodecanese',
    'ΛΕΣΒΟΥ': 'Lesbos',
    'ΧΙΟΥ': 'Chios',
    'ΣΑΜΟΥ': 'Samos',
    'ΗΡΑΚΛΕΙΟΥ': 'Heraklion',
    'ΧΑΝΙΩΝ': 'Chania',
    'ΡΕΘΥΜΝΟΥ': 'Rethymno',
    'ΛΑΣΙΘΙΟΥ': 'Lasithi',
    'ΚΕΡΚΥΡΑΣ': 'Corfu',
    'ΛΕΥΚΑΔΟΣ': 'Lefkada',
    'ΚΕΦΑΛΛΟΝΙΑΣ': 'Cephalonia',
    'ΖΑΚΥΝΘΟΥ': 'Zakynthos'
    }
    return region.apply(lambda x: region_mapping[x] if not pd.isna(x) else "")

def create_json(df):
    ''' create json response '''
    df['openYear'], df['openMonth'], df['openDay'], df['openDate'] = create_open_date(df['Ημερ/νία Έναρξης'])
    df['closeYear'], df['closeMonth'], df['closeDay'], df['closeDate'] = create_close_date(df['Ημερ/νία Κατασβεσης'])
    df['openTime'] ,df['closeTime'] = create_time(df['Ώρα Έναρξης']), create_time(df['Ώρα Κατάσβεσης'])
    df['damagedLand'] = sum_columns(df[['Δάση', 'Δασική Έκταση', 'Άλση', 'Χορτ/κές Εκτάσεις', 'Καλάμια - Βάλτοι', 'Γεωργικές Εκτάσεις', 'Υπολλείματα Καλλιεργειών', 'Σκουπι-δότοποι']])
    df['fireFighters'] = sum_columns(df[['ΠΥΡΟΣ. ΣΩΜΑ', 'ΠΕΖΟΠΟΡΑ ΤΜΗΜΑΤΑ']]).astype('int')
    df['volunteers'] = df['ΕΘΕΛΟ-ΝΤΕΣ'].apply(lambda x: int(x) if not pd.isna(x) else "")
    df['army'] = df['ΣΤΡΑΤΟΣ'].apply(lambda x: int(x) if not pd.isna(x) else "")
    df['otherForces'] = df['ΑΛΛΕΣ ΔΥΝΑΜΕΙΣ'].apply(lambda x: int(x) if not pd.isna(x) else "")
    df['fireTrucks'] = df['ΠΥΡΟΣ. ΟΧΗΜ.'].apply(lambda x: int(x) if not pd.isna(x) else "")
    df['otherVehicles'] = sum_columns(df[['ΟΧΗΜ. ΟΤΑ', 'ΒΥΤΙΟ- ΦΟΡΑ', 'ΜΗΧΑΝΗ-ΜΑΤΑ']]).astype('int')
    df['helicopters'] = df['ΕΛΙΚΟ- ΠΤΕΡΑ'].apply(lambda x: int(x) if not pd.isna(x) else "")
    df['airplanes'] = sum_columns(df[['Α/Φ CL415', 'Α/Φ CL215', 'Α/Φ PZL', 'Α/Φ GRU.']]).astype('int')
    df['country'] = 'Greece'
    df['emergencyTypeEnum'] = 'FIRE'
    df['locationType'] = 'Non-residential'
    df['region'] = map_region(df['Νομός'])
    df['database'] = 'Hellenic Fire Service (Forest)'
    result = df.loc[:, 'openYear':].to_json(orient='records')
    response = json.loads(result)
    return response

def return_json(list_of_files):
    ''' return json response '''
    df = create_dataframe(list_of_files)
    response = create_json(df)
    return response

