from rest_framework import viewsets
from rest_framework_gis import filters

from web.models import Station
from web.serializers import StationSerializer

import requests


class StationViewSet(viewsets.ReadOnlyModelViewSet):
    #query = """{
    #        bikeRentalStations {
    #        name
    #        stationId
    #    }
    #}"""
    #url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
    #r = requests.post(url, json={'query': query})
    
    bbox_filter_field = "point"
    filter_backends = (filters.InBBoxFilter,)
    queryset = Station.objects.all()
    print(queryset)
    print(queryset.values)
    serializer_class = StationSerializer
