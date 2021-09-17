

base_url = "http://si0vmc1343.de.bosch.com:8080/Thingworx/Runtime/index.html"


import requests

def get_pw_session(username=None, password=None):
    if username is None:
        with open("tests/credentials.txt", "r") as f:
            data = f.readlines()
            username = data[0].strip()
            password = data[1].strip()

    c = requests.session()
    c.get(base_url, auth=requests.auth.HTTPBasicAuth(username, password))
    
    return c    
