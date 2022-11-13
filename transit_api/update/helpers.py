from .ping_mbta_api import ping_mbta_api

stops, last_modified = ping_mbta_api('https://api-v3.mbta.com/stops', None)

def get_parent_stop(stop_id):
    global stops 
    for stop in stops:
        if stop['id'] == stop_id:
            return stop['relationships']['parent_station']['data']['id']
    return stop_id