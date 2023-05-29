import urllib
import csv
import codecs
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import urllib3
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import login_to_site
from settings import DOWNLOAD_PATH
import zipfile
import datetime

# configure download options of webdrive
options = webdriver.ChromeOptions()
options.add_argument("---headless")
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
prefs = {"profile.default_content_settings.popups": 0,
            "download.default_directory": DOWNLOAD_PATH,
            "directory_upgrade": True}
options.add_experimental_option("prefs", prefs)

def get_canadian_disaster_database_data():
    """ get data of the Canadian Disaster Database """
    # TSV delimiter = '\t' = tab

    url = 'https://cdd.publicsafety.gc.ca/dl-eng.aspx?cultureCode=en-Ca&normalizedCostYear=1&dynamic=false'
    response = urllib.request.urlopen(url)
    data = list(csv.reader(codecs.iterdecode(response, 'utf-8'), delimiter='\t'))

    for i in range(len(data)-1):
        # all diasters should have the same fields-columns
        if len(data[i]) != len(data[0]):
            for j in range(len(data[0])-len(data[i])):
                data[i].append('')

    # delete faulty rows
    for i in reversed(range(1, len(data)-1)):
        if data[i][0] != 'Disaster' and data[i][0] != 'Incident':
            del data[i]

    return data

def get_hellenic_fire_service_forest_data():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = requests.get("https://www.fireservice.gr/el_GR/synola-dedomenon", verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    list_of_a_tags = soup.find_all('a', href=re.compile('(/documents/20184/412680/(Das))|(/documents/20184/1196606/(Das))'))
    links = [link for link in list_of_a_tags if 'xlsx' in link or '.xlsx' in link or ' .xlsx' in link]
    valid_links = ['https://www.fireservice.gr'+ link.get('href') for link in links]
    
    forest_fires = []
    for link in valid_links:
        req = requests.get(link, verify=False)
        match = re.search('Das.+xlsx', link)
        if match:
            filename = DOWNLOAD_PATH + '/' + match.group(0)
            forest_fires.append(filename)
            if not os.path.exists(filename):
                with open(filename, 'wb') as output:
                    output.write(req.content)
    
    
    return forest_fires

def get_hellenic_fire_service_residential_data():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    r = requests.get("https://www.fireservice.gr/el_GR/synola-dedomenon", verify=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    list_of_a_tags = soup.find_all('a', href=re.compile('(/documents/20184/412680/(Ast))|(/documents/20184/1196606/(Ast))'))
    links = [link for link in list_of_a_tags if 'xlsx' in link or '.xlsx' in link or ' .xlsx' in link]
    valid_links = ['https://www.fireservice.gr'+ link.get('href') for link in links]
    residential_fires = []
    for link in valid_links:
        req = requests.get(link, verify=False)
        match = re.search('Ast.+xlsx', link)
        if match:
            filename = DOWNLOAD_PATH + '/' + match.group(0)
            residential_fires.append(filename)
            if not os.path.exists(filename):
                with open(filename, 'wb') as output:
                    output.write(req.content)

    return residential_fires

def get_emdat(username, password):
    """ get data of EMDAT """
    
    driver = webdriver.Chrome(chrome_options=options)

    # login to emdat
    driver = login_to_site(driver, "https://public.emdat.be/login", "user", username, "password", password, "Log in")
    
    # redirect
    time.sleep(1)
    driver.get("https://public.emdat.be/data")
    time.sleep(1)
    # check if logged in
    try:
        print(driver.find_element_by_xpath('//*[@id="__next"]/div/ul/li[5]'))
    except Exception as ex:
        raise Exception("Wrong username/password combination")
    # download dataset
    driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div/div/div/div/div/button[1]/span[1]').click()

    # wait for file to get downloaded
    dl_wait = True
    while dl_wait:
        time.sleep(1)
        for fname in os.listdir(DOWNLOAD_PATH):
            if fname.endswith('.xlsx'):
                dl_wait = False
                
    
    # get data
    for fname in os.listdir(DOWNLOAD_PATH):
        if fname.endswith('.xlsx'):
            print(DOWNLOAD_PATH + '/' + fname)

            readfile = pd.read_excel(DOWNLOAD_PATH + '/' + fname, skiprows=6)
            readfile.to_csv(DOWNLOAD_PATH + '/' + 'emdat.csv', index = None, header=True)

            with codecs.open(DOWNLOAD_PATH + '/' + 'emdat.csv') as read_file:
                dataset = pd.read_csv(read_file, delimiter=',')

    
    # delete files
    time.sleep(2)
    for fname in os.listdir(DOWNLOAD_PATH):
        if fname.endswith('.xlsx'):
            os.remove(DOWNLOAD_PATH + '/' + fname)
            os.remove(DOWNLOAD_PATH + '/' + 'emdat.csv')
            
    driver.quit()
    return dataset

def get_gidd_data():
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("https://www.internal-displacement.org/database/displacement-data")
    content = driver.find_elements_by_xpath('//button[@class="btn btn-primary"]')[1]
    content.click()

    # wait for file to get downloaded
    dl_wait = True
    while dl_wait:
        time.sleep(1)
        for fname in os.listdir(DOWNLOAD_PATH):
            if fname.endswith('.xlsx'):
                dl_wait = False
                
    
    # get data
    for fname in os.listdir(DOWNLOAD_PATH):
        if fname.endswith('.xlsx'):
            path_to_xlsx_file = DOWNLOAD_PATH + '/' + fname
            path_to_zip_file = path_to_xlsx_file[:-4] + 'zip'
            os.rename(path_to_xlsx_file, path_to_zip_file)
            zin = zipfile.ZipFile (path_to_zip_file, 'r')
            new_zip_file = DOWNLOAD_PATH + '/' + 'new_zip_file.zip'
            zout = zipfile.ZipFile (new_zip_file, 'w')
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                if (item.filename != 'xl/styles.xml'):
                    zout.writestr(item, buffer)
            zout.close()
            zin.close()
            fixed_xlsx_file = new_zip_file[:-3] + 'xlsx'
            os.rename(new_zip_file, fixed_xlsx_file)
            df = pd.read_excel(fixed_xlsx_file)
            
    # delete files
    time.sleep(2)
    for fname in os.listdir(DOWNLOAD_PATH):
        if fname.endswith('.xlsx'):
            os.remove(fixed_xlsx_file)
            os.remove(path_to_zip_file)
   
    driver.quit()
    return df

def get_gdacs_data():
    features = []
    for year in range(1985, datetime.datetime.now().year + 1):
        r = requests.get(f'https://www.gdacs.org/gdacsapi/api/Events/geteventlist/SEARCH?fromDate={year}-01-01&toDate={year}-12-31')
        if r.status_code == 200:
            for feature in r.json()['features']:
                features.append(feature)
            print(f'Added {year} records')
    
    list_of_dict = [{'latitude': feature['geometry']['coordinates'][1],
                'longitude': feature['geometry']['coordinates'][0],
                'eventtype': feature['properties']['eventtype'],
                'description': feature['properties']['description'],
                'alertlevel': feature['properties']['alertlevel'],
                'alertscore': feature['properties']['alertscore'],
                'episodealertlevel': feature['properties']['episodealertlevel'],
                'episodealertscore': feature['properties']['episodealertscore'],
                'locationarea': feature['properties']['country'],
                'fromdate': feature['properties']['fromdate'],
                'todate': feature['properties']['todate'],
                'iso3': feature['properties']['iso3'],
                'severity': feature['properties']['severitydata']['severity'],
                'severitytext': feature['properties']['severitydata']['severitytext'],
                'severityunit': feature['properties']['severitydata']['severityunit']} for feature in features]
    df = pd.DataFrame(list_of_dict)
    return df