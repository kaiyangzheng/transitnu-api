from rest_framework import serializers
from .models import Train, Stop, Line, Prediction

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ('id', 'line', 'location', 'status', 'stop', 'trip', 'occupancy', 'speed', 'direction_id', 'last_update')

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ('id', 'name', 'location', 'municipality', 'street')
        
class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line 
        fields = ('id', 'name', 'color', 'direction_destinations', 'direction_names', 'line', 'polylines')

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ('trip_id', 'vehicle_id', 'stop_id', 'arrival_time', 'departure_time')