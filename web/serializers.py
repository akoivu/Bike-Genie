from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from web.models import Station

import requests
import json

def get_amount_list():
    query = """{
            bikeRentalStations {
            name
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

    amount_list = get_amount_list()
    amount = serializers.SerializerMethodField('_asd')

    def _asd(self, obj):
        for row in self.amount_list:
            if row['stationId'] == str(obj.id):
                return row['bikesAvailable']
        return 'Error getting number of available bikes'


    class Meta:
        fields = ("id", "name", "address", "amount")
        geo_field = "point"
        model = Station

    

