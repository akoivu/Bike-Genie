from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class WebMapView(TemplateView):
    template_name = "map.html"