
import os
# from tests.cookie_test import get_pw_session
import requests
requests.packages.urllib3.disable_warnings()

import pandas as pd

import numpy as np

base_url = "http://si0vmc1343.de.bosch.com:8080/Thingworx/Runtime/index.html"

def get_pw_session(username=None, password=None):
    if username is None:
        with open("tests/credentials.txt", "r") as f:
            data = f.readlines()
            username = data[0].strip()
            password = data[1].strip()

    c = requests.session()
    c.get(base_url, auth=requests.auth.HTTPBasicAuth(username, password))
    
    return c  


def skip_download_file(row):
    """
    add filter rules what files to download/skip
    TRUE - file will be skipped
    FALSE - file will be downloaded

    """
    fileending = row["fileName"][-4:]
    if fileending in [".stp"]:
        return False
    
    return True


def filter_by_version(entities):
    """
    filter only elements with the highest version AB > AA
    """
    results = []
    highest_version = None
    for index, entity in enumerate(entities):
        if index == 0:
            highest_version = entity["version"]
        else:
            current_version = entity["version"]
            if current_version > highest_version:
                highest_version = current_version
                
    for entity in entities:
        if entity["version"] == highest_version:
            results.append(entity)
    
    return results


#%%

headers = {
    "Host": "si0vmc1343.de.bosch.com:8080",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "de-DE",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://si0vmc1343.de.bosch.com:8080/Thingworx/Runtime/index.html",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "DNT": "1",
    "Connection": "keep-alive"
}


url = "http://si0vmc1343.de.bosch.com:8080/Thingworx/Things/General_PDMLink_Search/Services/PDMLinkSearch?Accept=application%2Fjson&_twsr=1&Content-Type=application%2Fjson"


#%%


def read_spec_file(filepath):
    dfs = pd.read_excel(filepath, sheet_name=None)
    material_numbers = dfs["matnumbers"]
    return material_numbers


def search_mat_nr(mat_nr, session):
    
    search_req = {
        "Number":"",
        "RBMATNO":mat_nr,
        "RBPARTNOTITLE1":"",
        "RBSHORTDESCRIPTION":"",
        "docType":"All",
        "Filename":"",
        "RBLEGACYNUMBER":""
    }
    
    res = session.post(url, json=search_req, headers=headers)
    res_info = res.json()
    
    entities = []
    for data_row in res_info["rows"]:
        if "CADName" in data_row and \
            int(data_row["state--state"]) == 40:
                entities.append({
                "version": data_row["versionInfo--identifier--versionId"], 
                "filename": data_row["CADName"], 
                "link": data_row["obid"],
                "name" : data_row["RBSHORTDESCRIPTION"]
                })
    return entities

#%%

def download_file(entities, session, matnr):
    
    filtered_entities = filter_by_version(entities)
    print("  filtered {0} of {1} results".format(len(filtered_entities), len(entities)))
    available = False

    # list files
    file_url = "http://si0vmc1343.de.bosch.com:8080/Thingworx/Things/General_PDMLink_Search/Services/ListContentWithDataShape?Accept=application%2Fjson&_twsr=1&Content-Type=application%2Fjson"
    
    # download files
    for entity in filtered_entities:
        
        file_req_data = {"holderUfid": entity["link"]}
        res = session.post(file_url, json=file_req_data, headers=headers)
        res_file_info = res.json()

        for row in res_file_info["rows"]:
            
            if "urlLocation" not in row:
                print("skipping file in wrong context")
                continue
            
            fname = row["fileName"]
            print(f"name is : {fname}")
            
            download_url = row["urlLocation"]
            
            fpath = os.path.join("cache/windchill")
            print(f"name is : {fpath}")
            
            print(f"fpath of windchill - {fpath}")
            fullpath = os.path.join(fpath, fname)
            print(f"name is : {fullpath}")

            if skip_download_file(row):
                print("  {0} - {1} - skipped".format(matnr, row["fileName"]))
                continue
            elif os.path.isfile(fullpath):
                print("  {0} - {1} - file already available".format(matnr, row["fileName"]))
                available = True
                break
            
            res = session.get(download_url, headers=headers, verify=False)
            
            with open(fullpath, 'wb') as f:
                f.write(res.content)

            available = True
            print("  {0} - {1} - downloaded".format(matnr, row["fileName"]))
            break

        if available:
            break
    
    print(f"message from windchill -> available {available} and fullpath -> {fullpath}")
    return available, fullpath

def rasa_get_file(material_number):
    s = get_pw_session()   # s has the session
    
    entities = search_mat_nr(material_number, s)

    if len(entities):
        return download_file(entities, s, material_number)
        
    else:
        
        fullpath="Material number not found in windchill"
        available=False
        return available,fullpath

        



if __name__ == '__main__':

    material_number = "R901296755"
    
    available, filepath = rasa_get_file(material_number)

    print(f"{material_number} - {available} at {filepath}")    
# %%

def download_CAD(material_id):
    material_number = material_id
    available, filepath = rasa_get_file(material_number)
    return available,filepath
    
