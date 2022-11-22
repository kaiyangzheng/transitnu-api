from django.urls import path
from .views import (
    TrainList, 
    StopList, 
    LineList, 
    TrainDetail, 
    StopDetail, 
    LineDetail, 
    TrainByLine,
    PredictionList,
    PredictionDetail,
    PredictionByTrain,
    PredictionByStop
)

urlpatterns = [
    path('train/', TrainList.as_view(), name="train-list"),
    path('train/<train_id>', TrainDetail.as_view(), name="train-detail"),
    path('train/line/<line_id>', TrainByLine.as_view(), name="train-by-line"),
    path('stop/', StopList.as_view(), name="stop-list"),
    path('stop/<stop_id>', StopDetail.as_view(), name="stop-detail"),
    path('line/', LineList.as_view(), name="line-list"),
    path('line/<line_id>', LineDetail.as_view(), name="line-detail"),
    path('prediction/', PredictionList.as_view(), name="prediction-list"),
    path('prediction/<prediction_id>', PredictionDetail.as_view(), name="prediction-detail"),
    path('prediction/train/<train_id>', PredictionByTrain.as_view(), name="prediction-by-train"),
    path('prediction/stop/<stop_id>', PredictionByStop.as_view(), name="prediction-by-stop")

]