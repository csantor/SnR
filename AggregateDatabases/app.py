import os
import sys
import logging
import requests
import urllib
import csv
import codecs
import uvicorn
import numpy as np
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, Request
from database_loaders import get_canadian_disaster_database_data, get_hellenic_fire_service_forest_data, get_hellenic_fire_service_residential_data, get_emdat, get_gidd_data, get_gdacs_data
from databases import cdd, glc, hfs_forest, hfs_residential, usgs, emdat_db, gidd, gdacs



app = FastAPI()

class Credentials(BaseModel):
    username: str
    password: str


@app.get("/canadian_disaster_database")
def canadian_disaster_database():
    """get and return the data of the Canadian Disaster Database (CDD)"""
    try:
        print("canadian_disaster_database")
        # get input
        data_string = get_canadian_disaster_database_data()
        data = cdd.main(data_string)
        return data
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400

@app.get("/hellenic_fire_service_forest")
def hellenic_fire_service_forest():
    """get and return the data of the Hellenic Fire Service (Forest)"""
    try:
        forest_fires = get_hellenic_fire_service_forest_data()
        response = hfs_forest.return_json(forest_fires)
        return response
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400

@app.get("/hellenic_fire_service_residential")
def hellenic_fire_service_residential():
    """get and return the data of the Hellenic Fire Service (Residential)"""
    try:
        residential_fires = get_hellenic_fire_service_residential_data()
        response = hfs_residential.return_json(residential_fires)
        return response
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400

@app.get("/global_landslide_catalog")
def global_landslide_catalog():
    """get and return the data of the Global Landslide Catalog"""
    try:
        response = glc.return_json()
        return response
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400

@app.get("/usgs_earthquake_program")
def usgs_earthquake_program():
    """get and return the data of the USGS Earthquake Program"""
    try:
        response = usgs.return_json()
        return response
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400

@app.post("/emdat")
def emdat(credentials: Credentials):
    """get and return the data of the EMDAT"""
    try:
        print("emdat")
        # get input
        dataset = get_emdat(credentials.username, credentials.password)
        data = emdat_db.main(dataset)
        return data
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400

@app.get("/global_internal_displacement_database")
def global_internal_displacement_database():
    """get and return the data of the Global Internal Displacement Database"""
    try:
        print('gidd')
        df = get_gidd_data()
        response = gidd.return_json(df)
        return response
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400

@app.get("/global_disaster_alerting_coordination_system")
def global_disaster_alerting_coordination_system():
    """get and return the data of the Global Disaster Alerting Coordination System"""
    try:
        print('gdacs')
        df = get_gdacs_data()
        response = gdacs.return_json(df)
        return response
    except Exception as ex:
        logging.error(ex)
        return str(ex).encode('utf-8'), 400