from django.urls import path
from .views import TrainList, StopList, LineList, TrainDetail, StopDetail, LineDetail, TrainByLine

urlpatterns = [
    path('train/', TrainList.as_view(), name="train-list"),
    path('train/<train_id>', TrainDetail.as_view(), name="train-detail"),
    path('train/line/<line_id>', TrainByLine.as_view(), name="train-by-line"),
    path('stop/', StopList.as_view(), name="stop-list"),
    path('stop/<stop_id>', StopDetail.as_view(), name="stop-detail"),
    path('line/', LineList.as_view(), name="line-list"),
    path('line/<line_id>', LineDetail.as_view(), name="line-detail")

]