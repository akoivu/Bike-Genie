from django.urls import path
from .views import WebMapView

APP_NAME = 'web'

urlpatterns = [
    path('map/', WebMapView.as_view())
]
