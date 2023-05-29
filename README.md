# Search and Rescue - Aggregation of data coming from resources relevant to past large-scale disasters

This tool connects to existing databases relevant to past to past European/international large-scale disasters.  
As of now the following databases have been used:   
- Canadian Disaster Databases (CDD)
- EM-DAT
- USGS Earthquake Program
- Hellenic Fire Service (Forest)
- Hellenic Fire Service (Residential)
- Global Landslide Catalog (GLC)
- Global Internal Displacement Database (GIDD)

You can access this SnR tool from port `7070`.  

## Docker Installation

1. In case you are not in the snr directory run the following command: `cd snr`
2. To install our SnR tool using docker run the following command: `docker-compose up -d --build`

## APIs

### Access points:

1. Canadian Disaster Databases (CDD): `http://127.0.0.1:7070/canadian_disaster_database`
2. EM-DAT: `http://127.0.0.1:7070/emdat`
3. USGS Earthquake Program: `http://127.0.0.1:7070/usgs_earthquake_program`
4. Hellenic Fire Service (Forest): `http://127.0.0.1:7070/hellenic_fire_service_forest`
5. Hellenic Fire Service (Residential): `http://127.0.0.1:7070/hellenic_fire_service_residential`
6. Global Landslide Catalog (GLC): `http://127.0.0.1:7070/global_landslide_catalog`
7. Global Internal Displacement Database (GIDD): `http://127.0.0.1:7070/global_internal_displacement_database`

All requests are `GET` requests, except for the EM-DAT request that is a `POST` because anyone that wishes to access EM-DAT has to have previously registered in the platform and send his credentials for authorization.

<br/>

### Responses

<br/>

1. Canadian Disaster Database

`GET http://127.0.0.1:7070/canadian_disaster_database`

{<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "emergencyTypeEnum": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "description": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "database": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "openYear": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "openMonth": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "openDay": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "openDate": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "closeYear": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "closeMonth": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "closeDay": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "closeDate": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "country": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "locationType": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "vehicleType": `string`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "magnitude": `float`, <br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "casualties": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "injuredPeopleNumber": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "infectedPeopleNumber": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "evacuatedPeopleNumber": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "affectedPeopleNumber": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "damages": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "payments": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "insurancePayments": `int`,<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;    "currency": `string`<br/>
}

2. EM-DAT

`POST http://127.0.0.1:7070/emdat`

{<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;emergencyTypeEnum: `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;name: `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;database `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openYear: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openMonth: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openDay: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openTime: `datetime.time`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;closeYear: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;closeMonth: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;closeDay: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;iso: `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;country: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;locationArea: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;longitude: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;latitude: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;locationType: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;vehicleType: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;cause: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;linkedEmergencies: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;magnitude: `float`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;magnitudeMeasurementUnit: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;riverBasin: `string`<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;casualties: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;injuredPeopleNumber: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;homelessPeopleNumber: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;affectedPeopleNumber: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;payments: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;damages: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;insuredDamages: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;reconstructionCosts: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;currency: `string`<br/>
}

3. USGS Earthquake Program

`GET http://127.0.0.1:7070/usgs_earthquake_program`

{<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;database: `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;emergencyTypeEnum: `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openYear: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openMonth: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openDay: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openTime: `datetime.time`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;openDate: `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;latitude: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;longitude: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;depth: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;magnitude: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;gap: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;dmin: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;rms: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;locationArea: `string`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;horizontalError: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;depthError: `int`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;magError: `float`,<br/>
   &nbsp;&nbsp;&nbsp;&nbsp;country: `string`<br/>
}

4. Hellenic Fire Service (Forest)

`GET http://127.0.0.1:7070/hellenic_fire_service_forest`

{<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openYear: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openMonth: `int`,<br>
 &nbsp;&nbsp;&nbsp;&nbsp;openDay: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openDate: `string`<br>
 &nbsp;&nbsp;&nbsp;&nbsp;closeYear: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;closeMonth: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;closeDay: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;closeDate: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;openTime: `datetime.time`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;closeTime: `datetime.time`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;damagedLand: `float`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;fireFighters: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;volunteers: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;army: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;otherForces: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;fireTrucks: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;otherVehicles: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;helicopters: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;airplanes: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;country: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;emergencyTypeEnum: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;locationType: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;region: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;database: `string`<br/>
 }

 5. Hellenic Fire Service (Residential)

 `GET http://127.0.0.1:7070/hellenic_fire_service_residential`

 {<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openYear: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openMonth: `int`,<br>
 &nbsp;&nbsp;&nbsp;&nbsp;openDay: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openDate: `string`<br>
 &nbsp;&nbsp;&nbsp;&nbsp;closeYear: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;closeMonth: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;closeDay: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;closeDate: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;openTime: `datetime.time`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;closeTime: `datetime.time`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;fireFighters: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;fireTrucks: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;fireShips: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;country: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;emergencyTypeEnum: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;locationType: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;region: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;involvedPeopleNumber: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;injuredPeopleNumber: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;casualties: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;severity: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;database: `string`<br/>
 }

 6. Global Landslide Catalog

 `GET http://127.0.0.1:7070/global_landslide_catalog`

 {<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;database: `string`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;reportedDate: `datetime.date`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;title: `string`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;description: `string`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;cause: `string`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;severity: `string`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openYear: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openMonth: `int`,<br>
 &nbsp;&nbsp;&nbsp;&nbsp;openYear: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openDate: `string`<br>
&nbsp;&nbsp;&nbsp;&nbsp;openTime: `datetime.time`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;country: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;locationType: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;casualties: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;injuredPeopleNumber: `int`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;emergencyTypeEnum: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;latitude: `float`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;longitude: `float`<br/>
}

7. Global Internal Displacement Database

`GET http://127.0.0.1:7070/global_internal_displacement_database`

 {<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;database: `string`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;country: `string`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openYear: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openMonth: `int`,<br>
 &nbsp;&nbsp;&nbsp;&nbsp;openDay: `int`,<br/>
 &nbsp;&nbsp;&nbsp;&nbsp;openDate: `string`<br>
&nbsp;&nbsp;&nbsp;&nbsp;description: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;emergencyTypeEnum: `string`,<br/>
&nbsp;&nbsp;&nbsp;&nbsp;evacuatedPeopleNumber: `int`<br/>}
