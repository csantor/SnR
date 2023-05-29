import numpy as np
import json
import datetime

def convert_float(data, number):
    """ check if string is NULL and if not convert it to float """
    if data == "nan":
        return
    else:
        return float(data)*number

def convert_int(data):
    """ check if string is NULL and if not convert it to int """
    if data == "nan":
        return
    else:
        return int(round(float(data)))

def determineEmergencyType(disaster_type, disaster_subtype):
    """ determine SnR disaster type """
    
    if disaster_subtype == 'Avalanche':
        emergencyType = "AVALANCHE"
    elif disaster_subtype in ['Gas leak', 'Chemical spill', 'Poisoning', 'Oil spill']:
        emergencyType = 'CHEMICAL'
    elif disaster_subtype == 'Collapse':
        emergencyType = "COLLAPSE"
    elif disaster_type == 'Epidemic':
        emergencyType = "EPIDEMY"
    elif disaster_type == 'Flood':
        emergencyType = "FLOOD"
    elif disaster_type == 'Storm':
        emergencyType = "STORM"
    elif disaster_type == 'Transport accident':
        emergencyType = "TRANSPORTATION"
    elif disaster_subtype == 'Tsunami':
        emergencyType = "TSUNAMI"
    elif disaster_type == 'Volcanic activity':
        emergencyType = "VOLCANO"
    elif disaster_type == 'Wildfire' or disaster_subtype in ['Explosion', 'Fire']:
        emergencyType = "FIRE"
    elif disaster_type == 'Landslide' or disaster_subtype in ['Rockfall', 'Landslide']:
        emergencyType = "LANDSLIDE"
    elif disaster_type in ['Mass movement (dry)', 'Earthquake']:
        emergencyType = "EARTHQUAKE"
    else:
        emergencyType = ""
    return emergencyType

def determineLocationType(disaster_type, disaster_subtype):
    if disaster_type == 'Industrial accident':
        return "Industrial"
    elif disaster_subtype in ['Forest fire', 'Land fire (Brush, Bush, Pasture)']:
        return "Natural Open Space"
    elif disaster_type == 'Transport accident':
        return 'Vehicle'
    else:
        return ""

def determineVehicleType(disaster_subtype):
    if disaster_subtype in ['Air', 'Rail', 'Road']:
        return disaster_subtype
    elif disaster_subtype == 'Water':
        return 'Marine'
    else:
        return ""

def determineLinkedEmergencies(emergency1, emergency2):
    if emergency1 == "nan" and emergency2 == "nan":
        return ""
    elif emergency1 == "nan":
        return emergency2
    elif emergency2 == "nan":
        return emergency1
    else:
        return emergency1 + ', ' + emergency2

def create_json(data):
    """ create json object for each disaster """

    name = "" if str(data['Event Name']) == "nan" else str(data['Event Name'])
    locationArea = "" if str(data['Location']) == "nan" else str(data['Location'])
    country = "" if str(data['Country']) == "nan" else str(data['Country'])
    iso = "" if str(data['ISO']) == "nan" else str(data['ISO'])
    magnitudeMeasurementUnit = "" if str(data['Dis Mag Scale']) == "nan" else str(data['Dis Mag Scale'])
    cause = "" if str(data['Origin']) == "nan" else str(data['Origin'])
    riverBasin = "" if str(data['River Basin']) == "nan" else str(data['River Basin'])
    openYear = convert_int(str((data['Start Year'])))
    openMonth =  convert_int(str((data['Start Month'])))
    openDay = convert_int(str((data['Start Day'])))
    closeYear = convert_int(str((data['End Year'])))
    closeMonth =  convert_int(str((data['End Month'])))
    closeDay = convert_int(str((data['End Day'])))
    openTime = "" if str(data['Local Time']) == "nan" else str(data['Local Time'])
    linkedEmergencies = determineLinkedEmergencies(str(data['Associated Dis']), str(data['Associated Dis2']))
    longitude = "" if str(data['Longitude']) == "nan" else str(data['Longitude'])
    latitude = "" if str(data['Latitude']) == "nan" else str(data['Latitude'])

    json_object = {
        "emergencyTypeEnum": determineEmergencyType(data['Disaster Type'], data['Disaster Subtype']),
        "name": name,
        "database": "EMDAT",
        "openYear": openYear,
        "openMonth": openMonth,
        "openDay": openDay,
        "openTime": openTime,
        "closeYear": closeYear,
        "closeMonth": closeMonth,
        "closeDay": closeDay,
        "iso": iso,
        "country": country,
        "locationArea": locationArea,
        "longitude": longitude,
        "latitude": latitude,
        "locationType": determineLocationType(data['Disaster Type'], data['Disaster Subtype']),
        "vehicleType": determineVehicleType(data['Disaster Subtype']),
        "cause": cause,
        "linkedEmergencies": linkedEmergencies,
        "magnitude": convert_float(str((data['Dis Mag Value'])), 1),
        "magnitudeMeasurementUnit": magnitudeMeasurementUnit,
        "riverBasin": riverBasin,
        "casualties": convert_int(str((data['Total Deaths']))),
        "injuredPeopleNumber": convert_int(str((data['No Injured']))),
        "homelessPeopleNumber": convert_int(str((data['No Homeless']))),
        "affectedPeopleNumber": convert_int(str((data['No Affected']))),
        "payments": convert_float(str((data['Aid Contribution'])), 1000),
        "damages": convert_float(str((data['Total Damages (\'000 US$)'])), 1000),
        "insuredDamages": convert_float(str((data['Insured Damages (\'000 US$)'])), 1000),
        "reconstructionCosts": convert_float(str((data['Reconstruction Costs (\'000 US$)'])), 1000),
        "currency": "USD"
    }

    return json_object

def main(data):
    """ transform and return cdd data """
    response = []
    for i in range(len(data["Year"])):
        json_object = create_json(data.iloc[i])
        if json_object["emergencyTypeEnum"] != "":
            response.append(json_object)

    return response
