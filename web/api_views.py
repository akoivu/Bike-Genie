from rest_framework import viewsets
from rest_framework_gis import filters

from web.models import Station
from web.serializers import StationSerializer


class StationViewSet(viewsets.ReadOnlyModelViewSet):

    bbox_filter_field = "point"
    filter_backends = (filters.InBBoxFilter,)
    queryset = Station.objects.all()
    serializer_class = StationSerializer
