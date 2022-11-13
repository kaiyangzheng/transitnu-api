from django.contrib import admin
from .models import Train, Line, Stop, Prediction

# Register your models here.
admin.site.register(Train)
admin.site.register(Line)
admin.site.register(Stop)
admin.site.register(Prediction)
