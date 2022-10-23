from rest_framework import serializers
from .models import Train
from .models import Stop
from .models import Line

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ('id', 'line', 'location', 'status', 'stop', 'occupancy', 'speed', 'last_update')

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ('id', 'name', 'location', 'municipality', 'street')
        
class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line 
        fields = ('id', 'name', 'color', 'direction_destinations', 'direction_names', 'line', 'polylines')