import requests

API_KEY = "be776a7b62b948339f29cc2bd403e016"

def ping_mbta_api(url, if_modified_since):
    r = requests.get(url, headers={'x-api-key' : API_KEY, 'if-modified-since': if_modified_since})
    headers = r.headers
    last_modified = headers['last-modified']
    if (r.status_code == 304):
        return [], last_modified
    data = r.json()
    data = data['data']
    return data, last_modified

def ping_mbta_api_raw(url, if_modified_since):
    r = requests.get(url, headers={'x-api-key' : API_KEY, 'if-modified-since': if_modified_since})
    headers = r.headers
    last_modified = headers['last-modified']
    if (r.status_code == 304):
        return [], last_modified
    data = r.json()
    return data, last_modified