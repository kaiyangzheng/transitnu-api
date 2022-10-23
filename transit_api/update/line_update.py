from ..models import Line 
from .ping_mbta_api import ping_mbta_api, ping_mbta_api_raw

def update_line_info(if_modified_since):
    lines, last_modified = ping_mbta_api('https://api-v3.mbta.com/routes', if_modified_since)
    if len(lines) == 0:
        return last_modified
    for line in lines:
        line_id = line['id']
        line_info = line['attributes']
        if (line_info['type'] != 1 and line_info['type'] != 0):
            continue
        line_db = Line.objects.filter(id=line_id)
        if not line_db:
            new_line = Line(
                id=line_id,
                name=line_info['long_name'],
                color=line_info['color'],
                direction_destinations=line_info['direction_destinations'],
                direction_names=line_info['direction_names'],
                line = line['relationships']['line']['data']['id'],
                polylines = get_polylines(line_id)
            )
            new_line.save()
        else:
            line_db.update(
                name=line_info['long_name'],
                color=line_info['color'],
                direction_destinations=line_info['direction_destinations'],
                direction_names=line_info['direction_names'],
                line = line['relationships']['line']['data']['id'],
                polylines = get_polylines(line_id)
            )
    return last_modified

def get_polylines(line_id):
    route_shape, last_modified = ping_mbta_api_raw(f'https://api-v3.mbta.com/routes/{line_id}?include=route_patterns.representative_trip.shape', None)
    polylines = []
    if 'included' not in route_shape.keys():
        return []
    route_shape = route_shape['included']
    for shape in route_shape:
        if 'polyline' in shape['attributes']:
            polylines.append(shape['attributes']['polyline'])
    return polylines