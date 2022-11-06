from ..models import Train, Stop, Line 
from ..serializers import StopSerializer, LineSerializer
from .ping_mbta_api import ping_mbta_api

def update_train_info(if_modified_since0, if_modified_since1):
    trains0, last_modified0 = ping_mbta_api('https://api-v3.mbta.com/vehicles/?filter%5Broute_type%5D=0', if_modified_since0)
    trains1, last_modified1 = ping_mbta_api('https://api-v3.mbta.com/vehicles/?filter%5Broute_type%5D=1', if_modified_since1)
    trains = trains0 + trains1
    if trains == []:
        return last_modified0, last_modified1
    train_ids = []
    for train in trains:
        train_ids.append(train['id'])
    for train in trains:
        train_id = train['id']
        train_info = train['attributes']
        train_rels = train['relationships']
        stop_data = train_rels['stop']['data']
        line_data = train_rels['route']['data']
        stop = None 
        if stop_data:
            stop = Stop.objects.filter(id=stop_data['id'])
            if stop.count() > 0:
                stop = stop[0]
            else:
                stop = None
        stop_serializer = StopSerializer(stop)
        line = None
        if line_data:
            line = Line.objects.filter(id=line_data['id'])
            if line.count() > 0:
                line = line[0]
            else:
                line = None
        line_serializer = LineSerializer(line)
        train_db = Train.objects.filter(id=train_id)
        if not train_db:
            new_train = Train(
                id = train_id,
                line = line_serializer.data,
                location = {
                    'longitude': train_info['longitude'],
                    'latitude': train_info['latitude'],
                    'bearing': train_info['bearing']
                },
                status = train_info['current_status'],
                stop = stop_serializer.data,
                occupancy = train_info['occupancy_status'],
                speed = train_info['speed'],
                direction_id = train_info['direction_id'],
                last_update = train_info['updated_at']
            )
            new_train.save()
        else:
            print(train_ids)
            print(train_db[0].id)
            print(train_db[0].direction_id)
            if (train_db[0].id not in train_ids):
                train_db.delete()
            else:
                train_db.update(
                    line = line_serializer.data,
                    location = {
                        'longitude': train_info['longitude'],
                        'latitude': train_info['latitude'],
                        'bearing': train_info['bearing']
                    },
                    status = train_info['current_status'],
                    stop = stop_serializer.data,
                    occupancy = train_info['occupancy_status'],
                    speed = train_info['speed'],
                    direction_id = train_info['direction_id'],
                    last_update = train_info['updated_at']
                )
    return last_modified0, last_modified1 



