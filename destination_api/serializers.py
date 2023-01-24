from rest_framework import serializers

from workspace.models import Destination


class DestinationCityCountrySerializer(serializers.ModelSerializer):
    """
    Serializer used for the DestinationCityCountryListAPI() api
    """
    class Meta: 
        model = Destination
        fields = (
            'city', 
            'country'
        )


class DestinationCityCountSerializer(serializers.ModelSerializer):
    """
    Serializer used for the DestinationCityCountListAPI() api
    """
    count = serializers.IntegerField()

    class Meta:
        model = Destination
        fields = (
            'city',
            'count'
        )


class DestinationCityActivitySerializer(serializers.ModelSerializer):
    """
    Serializer used for the DestinationCityActivityListAPI() api
    """
    class Meta:
        model = Destination
        fields = (
            'city',
            'activity1',
            'activity2',
            'activity3',
            'activity4' 
        )
