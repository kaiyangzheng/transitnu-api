from ..models import Stop, Line
from ..serializers import LineSerializer
from .ping_mbta_api import ping_mbta_api

def update_stop_info(if_modified_since):
    stops, last_modified = ping_mbta_api("https://api-v3.mbta.com/stops", if_modified_since)
    if (len(stops)) == 0:
        return last_modified
    for stop in stops:
        stop_id = stop['id']
        stop_info = stop['attributes']
        stop_db = Stop.objects.filter(id=stop_id)
        if not stop_db:
            new_stop = Stop(
                id=stop_id,
                name=stop_info['name'],
                location={
                    'longitude': stop_info['longitude'],
                    'latitude': stop_info['latitude']
                },
                municipality=stop_info['municipality'],
                street=stop_info['on_street'],
            )
            new_stop.save()
        else:
            stop_db.update(
                name=stop_info['name'],
                location={
                    'longitude': stop_info['longitude'],
                    'latitude': stop_info['latitude']
                },
                municipality=stop_info['municipality'],
                street=stop_info['on_street'],
            )
    return last_modified

