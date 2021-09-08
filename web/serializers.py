from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from web.models import Station

import requests
import json

def get_bike_availability_list():
    query = """{
            bikeRentalStations {
            stationId
            bikesAvailable
        }
    }"""
    url = 'https://api.digitransit.fi/routing/v1/routers/hsl/index/graphql'
    r = requests.post(url, json={'query': query})
    json_data = json.loads(r.text)
    data = json_data['data']['bikeRentalStations']
    return data

class StationSerializer(GeoFeatureModelSerializer):

    amount_list = get_bike_availability_list()
    amount = serializers.SerializerMethodField('_get_number_of_available_bikes')

    def _get_number_of_available_bikes(self, obj):
        for row in self.amount_list:
            if int(row['stationId']) == obj.id:
                return row['bikesAvailable']
        return 'Error getting number of available bikes'

    class Meta:
        fields = ("id", "name", "address", "amount")
        geo_field = "point"
        model = Station

    

