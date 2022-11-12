from ..models import Train, Stop, Line 
from ..serializers import StopSerializer, LineSerializer
from .ping_mbta_api import ping_mbta_api

def update_train_info(if_modified_since):
    trains, last_modified = ping_mbta_api('https://api-v3.mbta.com/vehicles/?filter%5Broute_type%5D=0,1', if_modified_since)
    if trains == []:
        return last_modified
    train_ids = []
    for train in trains:
        train_ids.append(train['id'])
    for train in trains:
        train_id = train['id']
        train_info = train['attributes']
        train_rels = train['relationships']
        stop_data = train_rels['stop']['data']
        trip_data = train_rels['trip']['data']
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
        predictions = []
        if trip_data:
            trip_id = trip_data['id']
            trip_predictions, last_modified_prediction = ping_mbta_api(f'https://api-v3.mbta.com/predictions?filter[trip]={trip_id}', if_modified_since)
            for prediction in trip_predictions:
                predict_stop = Stop.objects.filter(id=prediction['relationships']['stop']['data']['id'])
                predict_stop_serializer = StopSerializer(predict_stop)
                predictions.append({
                    'arrival_time': prediction['attributes']['arrival_time'],
                    'departure_time': prediction['attributes']['departure_time'],
                    'stop': predict_stop_serializer.data
                })
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
                trip = trip_data['id'],
                predictions = predictions,
                occupancy = train_info['occupancy_status'],
                speed = train_info['speed'],
                direction_id = train_info['direction_id'],
                last_update = train_info['updated_at']
            )
            new_train.save()
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
                trip = trip_data['id'],
                predictions = predictions,
                occupancy = train_info['occupancy_status'],
                speed = train_info['speed'],
                direction_id = train_info['direction_id'],
                last_update = train_info['updated_at']
            )
    trains = Train.objects.all()
    for train in trains:
        if (train.id not in train_ids):
            train.delete()
    return last_modified



