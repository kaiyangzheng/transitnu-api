from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Train, Stop, Line, Prediction
from .serializers import LineSerializer, TrainSerializer, StopSerializer, PredictionSerializer

class TrainList(APIView):  
    permission_classes = [permissions.AllowAny]
    serializer_class = TrainSerializer
    http_method_names = ['get']

    def get(self, request):
        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrainDetail(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TrainSerializer
    http_method_names = ['get']

    def get(self, request, train_id):
        train = Train.objects.get(id=train_id)
        if not train:
            return Response(
                {},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TrainSerializer(train)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrainByLine(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TrainSerializer
    http_method_names =['get']

    def get(self, request, line_id):
        trains = Train.objects.filter(line__id=line_id)
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StopList(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StopSerializer
    http_method_names = ['get']

    def get(self, request):
        stops = Stop.objects.all()
        serializer = StopSerializer(stops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StopDetail(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = StopSerializer
    http_method_names = ['get']

    def get(self, request, stop_id):
        stop = Stop.objects.get(id=stop_id)
        if not stop:
            return Response(
                {},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = StopSerializer(stop)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LineList(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LineSerializer
    http_method_names = ['get']

    def get(self, request):
        lines = Line.objects.all()
        serializer = LineSerializer(lines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LineDetail(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LineSerializer 
    http_method_names = ['get']

    def get(self, request, line_id):
        line = Line.objects.get(id=line_id)
        if not line:
            return Response(
                {},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = LineSerializer(line)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PredictionList(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PredictionSerializer
    http_method_names = ['get']

    def get(self, request):
        predictions = Prediction.objects.all()
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PredictionDetail(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PredictionSerializer
    http_method_names = ['get']

    def get(self, request, prediction_id):
        prediction = Prediction.objects.get(id=prediction_id)
        if not prediction: 
            return Response(
                {},
                status = status.HTTP_400_BAD_REQUEST
            )
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PredictionByTrain(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PredictionSerializer
    http_method_names = ['get']

    def get(self, request, train_id):
        predictions = Prediction.objects.filter(vehicle_id=train_id)
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PredictionByStop(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PredictionSerializer
    http_method_names = ['get']

    def get(self, request, stop_id):
        predictions = Prediction.objects.filter(stop_id=stop_id)
        serializer = PredictionSerializer(predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    