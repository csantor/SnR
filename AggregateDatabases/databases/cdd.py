import numpy as np
import json
import datetime

def create_date(date):
    str_date = "" + date
    if date == "":
        return "", "", "", ""
    else:
        split_date = str_date.split(' ')
        year = int("" + ("" + split_date[0]).split('/')[2])
        month = int("" + ("" + split_date[0]).split('/')[0])
        day = int("" + ("" + split_date[0]).split('/')[1])
        final_date = ("" + str(datetime.datetime(year, month, day))).split(' ')[0]
        return year, month, day, final_date

def initial_fields(data):
    """ map cdd fields to columns """
    initial_field_columns = {}
    for i in range(len(data)):
        initial_field_columns[data[i]] = i
    return initial_field_columns

def check_int_null(data):
    """ check if string is NULL and if not convert it to int """
    if data == "":
        return 0
    else:
        return int("" + str((data)).split(".")[0])

def check_float_null(data):
    """ check if string is NULL and if not convert it to float """
    if data == "":
        return 0
    else:
        return float("" + str((data)).split(".")[0])

def get_column(data, i):
    """ get column i """
    column = [row[i] for row in data]
    return column

def calculate_payments(federal, provincial_dfa, provincial_department, insurance, ngo):
    """ calculate total payments """
    federal = check_float_null(federal)
    provincial_dfaa = check_float_null(provincial_dfa)
    provincial_department = check_float_null(provincial_department)
    insurance = check_float_null(insurance)
    ngo = check_float_null(ngo)
    return federal + provincial_dfaa + provincial_department + insurance + ngo

def determineLocationType(event_type):
    if event_type in ['Non-Residential', 'Residential', 'Vehicle']:
        return event_type
    else:
        return ""

def determineVehicleType(event_type):
    if event_type in ['Air', 'Marine', 'Rail', 'Road']:
        return event_type
    else:
        return ""

def disasterTypeMapping(type):
    """ map cdd disaster types to SnR disaster types """
    mapping = {
        "Epidemic": "EPIDEMY",
        "Infestation": "EPIDEMY",
        "Pandemic": "EPIDEMY",
        "Drought": "",
        "Wildfire": "FIRE",
        "Cold Event": "",
        "Heat Event": "",
        "Hurricane / Typhoon / Tropical Storm": "STORM",
        "Typhoon": "STORM",
        "Tropical Storm": "STORM",
        "Storm Surge": "STORM",
        "Storm - Unspecified / Other": "STORM",
        "Winter Storm": "STORM",
        "Storms and Severe Thunderstorms": "STORM",
        "Tornado": "STORM",
        "Geomagnetic Storm": "STORM",
        "Avalanche": "AVALANCHE",
        "Flood": "FLOOD",
        "Tsunami": "TSUNAMI",
        "Landslide": "LANDSLIDE",
        "Earthquake": "EARTHQUAKE",
        "Volcano": "VOLCANO",
        "Disturbance / Demonstrations": "",
        "Rioting": "",
        "Hijacking": "TERRORISM",
        "Biological": "TERRORISM",
        "Bomb Attacks": "TERRORISM",
        "Chemical": "TERRORISM",
        "False Alarm": "",
        "Hoax": "",
        "Kidnapping / Murder": "",
        "Nuclear": "TERRORISM",
        "Shootings": "TERRORISM",
        "Radiological": "TERRORISM",
        "Arson": "FIRE",
        "Explosion": "FIRE",
        "Fire": "FIRE",
        "Leak / Spill Release": "CHEMICAL",
        "Derailment Release": "CHEMICAL",
        "Vehicle Release": "CHEMICAL",
        "Marine Release": "CHEMICAL",
        "Transportation accident": "TRANSPORTATION",
        "Communications": "",
        "Energy": "",
        "Manufacturing / Industry": "",
        "Transportation": "TRANSPORTATION",
        "Water": "",
        "Space Debris": "",
        "Space Launch": ""
    }
    return mapping[type]

def determineEmergencyType(event_type, event_subgroup):
    """ determine SnR disaster type """
    if event_type in ['Air', 'Marine', 'Rail', 'Road', 'Non-Residential', 'Residential', 'Vehicle']:
        return disasterTypeMapping(event_subgroup)
    else:
        return disasterTypeMapping(event_type)

def create_json(data, fields):
    """ create json object for each disaster """

    openYear, openMonth, openDay, openDate = create_date(data[fields['EVENT START DATE']])
    closeYear, closeMonth, closeDay, closeDate = create_date(data[fields['EVENT END DATE']])
    emergencyType = determineEmergencyType(data[fields['EVENT TYPE']], data[fields['EVENT SUBGROUP']])
    if emergencyType == 'EPIDEMY':
        infectedPeopleNumber = check_int_null(data[fields['INJURED / INFECTED']])
        injuredPeopleNumber = 0
    else:
        injuredPeopleNumber = check_int_null(data[fields['INJURED / INFECTED']])
        infectedPeopleNumber = 0

    json_object = {
        "emergencyTypeEnum": emergencyType,
        "description": data[fields['COMMENTS']],
        "database": "Canadian Disaster Database (CDD)",
        "openYear": openYear,
        "openMonth": openMonth,
        "openDay": openDay,
        "openDate": openDate,
        "closeYear": closeYear,
        "closeMonth": closeMonth,
        "closeDay": closeDay,
        "closeDate": closeDate,
        "country": "Canada",
        "locationType": determineLocationType(data[fields['EVENT TYPE']]),
        "vehicleType": determineVehicleType(data[fields['EVENT TYPE']]),
        "magnitude": check_float_null(data[fields['MAGNITUDE']]),
        "casualties": check_int_null(data[fields['FATALITIES']]),
        "injuredPeopleNumber": injuredPeopleNumber,
        "infectedPeopleNumber": infectedPeopleNumber,
        "evacuatedPeopleNumber": check_int_null(data[fields['EVACUATED']]),
        "affectedPeopleNumber": check_int_null(data[fields['UTILITY - PEOPLE AFFECTED']]),
        "damages": check_float_null(data[fields['ESTIMATED TOTAL COST']]),
        "payments": calculate_payments(data[fields['FEDERAL DFAA PAYMENTS']], data[fields['PROVINCIAL DFAA PAYMENTS']], data[fields['PROVINCIAL DEPARTMENT PAYMENTS']], data[fields['INSURANCE PAYMENTS']], data[fields['NGO PAYMENTS']]),
        "insurancePayments": check_float_null(data[fields['INSURANCE PAYMENTS']]),
        "currency": "USD"
    }


    return json_object

def main(data):
    """ transform and return cdd data """
    fields = initial_fields(data[0])
    response = []
    for i in range(len(data[1:])):
        json_object = create_json(data[i+1], fields)
        if json_object["emergencyTypeEnum"] != "":
            response.append(json_object)

    return response
