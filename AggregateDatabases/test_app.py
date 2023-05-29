from logging import raiseExceptions
from fastapi.testclient import TestClient
from .app import app


client = TestClient(app)

def test_cdd():
    ''' test canadian disaster database for response code 200 and content type json '''
    response = client.get("/canadian_disaster_database")
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    assert isinstance(response.json()[0]['emergencyTypeEnum'], str)
    assert isinstance(response.json()[0]['description'], str)
    assert isinstance(response.json()[0]['database'], str)
    assert isinstance(response.json()[0]['openYear'], int)
    assert isinstance(response.json()[0]['openMonth'], int)
    assert isinstance(response.json()[0]['openDay'], int)
    assert isinstance(response.json()[0]['openDate'], str)
    assert isinstance(response.json()[0]['closeYear'], int)
    assert isinstance(response.json()[0]['closeMonth'], int)
    assert isinstance(response.json()[0]['closeDay'], int)
    assert isinstance(response.json()[0]['closeDate'], str)
    assert isinstance(response.json()[0]['country'], str)
    assert isinstance(response.json()[0]['locationType'], str)
    assert isinstance(response.json()[0]['vehicleType'], str)
    assert isinstance(response.json()[0]['magnitude'], float)
    assert isinstance(response.json()[0]['casualties'], int)
    assert isinstance(response.json()[0]['injuredPeopleNumber'], int)
    assert isinstance(response.json()[0]['infectedPeopleNumber'], int)
    assert isinstance(response.json()[0]['evacuatedPeopleNumber'], int)
    assert isinstance(response.json()[0]['affectedPeopleNumber'], int)
    assert isinstance(response.json()[0]['damages'], int)
    assert isinstance(response.json()[0]['currency'], str)

# def test_gidd():
#     ''' test global internal displacement database for response code 200 and content type json '''
#     response = client.get("/global_internal_displacement_database")
#     assert response.status_code == 200
#     assert response.headers['content-type'] == 'application/json'

# def test_glc():
#     ''' test global landslide catalog for response code 200 and content type json '''
#     response = client.get("/global_landslide_catalog")
#     assert response.status_code == 200
#     assert response.headers['content-type'] == 'application/json'

# def test_hfs_forest():
#     ''' test hellenic fire service (forest) for response code 200 and content type json '''
#     response = client.get("/hellenic_fire_service_forest")
#     assert response.status_code == 200
#     assert response.headers['content-type'] == 'application/json'

# def test_hfs_residential():
#     ''' test hellenic fire service (residential) for response code 200 and content type json '''
#     response = client.get("/hellenic_fire_service_residential")
#     assert response.status_code == 200
#     assert response.headers['content-type'] == 'application/json'

# def test_usgs():
#     ''' test USGS Earthquake program for response code 200 and content type json '''
#     response = client.get("/usgs_earthquake_program")
#     assert response.status_code == 200
#     assert response.headers['content-type'] == 'application/json'