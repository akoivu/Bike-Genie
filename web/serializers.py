from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from web.models import Station


class StationSerializer(GeoFeatureModelSerializer):

    bike_amount = serializers.BooleanField(source='get_number_of_bikes')
    class Meta:
        fields = ("id", "name", "address", "bike_amount")
        geo_field = "point"
        model = Station
