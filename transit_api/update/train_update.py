from ..models import Train, Stop, Line, Prediction
from ..serializers import StopSerializer, LineSerializer
from .ping_mbta_api import ping_mbta_api
from .helpers import get_parent_stop


def update_train_info(if_modified_since):
    trains, last_modified = ping_mbta_api('https://api-v3.mbta.com/vehicles/?filter%5Broute_type%5D=0,1', if_modified_since)
    if trains == []:
        return last_modified
    train_ids = []
    for train in trains:
        train_id = train['id']
        train_info = train['attributes']
        train_rels = train['relationships']
        stop_data = train_rels['stop']['data']
        line_data = train_rels['route']['data']
        train_ids.append(train_id)
        stop = None 
        if stop_data:
            stop = Stop.objects.filter(id=get_parent_stop(stop_data['id']))
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
                trip = train_rels['trip']['data']['id'],
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
                trip = train_rels['trip']['data']['id'],
                occupancy = train_info['occupancy_status'],
                speed = train_info['speed'],
                direction_id = train_info['direction_id'],
                last_update = train_info['updated_at']
            )
    trains = Train.objects.all()
    for train in trains:
        if (train.id not in train_ids):
            train.delete()

    prediction_ids = []
    for train in trains:
        trip_id = train.trip
        predictions, last_modified = ping_mbta_api(f'https://api-v3.mbta.com/predictions?filter[trip]={trip_id}', None)
        for prediction in predictions:
            prediction_info = prediction['attributes']
            prediction_rels = prediction['relationships']
            prediction_stop = get_parent_stop(prediction_rels['stop']['data']['id'])
            prediction_trip = prediction_rels['trip']['data']['id']
            prediction_vehicle = prediction_rels['vehicle']['data']['id']
            prediction_ids.append(
                [prediction_trip, prediction_vehicle, prediction_stop]
            )
            prediction_db = Prediction.objects.filter(trip_id=prediction_trip, vehicle_id=prediction_vehicle, stop_id=prediction_stop)
            if not prediction_db:
                new_prediction = Prediction(
                    trip_id=prediction_trip,
                    vehicle_id=prediction_vehicle,
                    stop_id=prediction_stop,
                    arrival_time=prediction_info['arrival_time'],
                    departure_time=prediction_info['departure_time']
                )
                new_prediction.save()
            else:
                prediction_db.update(
                    arrival_time=prediction_info['arrival_time'],
                    departure_time=prediction_info['departure_time']
                )
    prediction = Prediction.objects.all()
    for predictions in prediction:
        if [prediction.trip_id, prediction.vehicle_id, prediction.stop_id] not in prediction_ids:
            prediction.delete()
    return last_modified



