from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    DestinationCityCountrySerializer, 
    DestinationCityCountSerializer, 
    DestinationCityActivitySerializer
)
from workspace.models import Destination
from django.db.models import Count


@permission_classes([IsAuthenticated])
class DestinationCityCountryListAPI(generics.ListAPIView):
    """
    API endpoint returns destinations created by all users.
    Queryset includes city and country.
    """
    queryset = Destination.destination_objects.values(
        'city', 
        'country'
    ).distinct()
    serializer_class = DestinationCityCountrySerializer


@permission_classes([IsAuthenticated])
class DestinationCityCountListAPI(generics.ListAPIView):
    """
    API endpoint returns the most created city by all users.
    Queryset includes city and count.
    """
    queryset = Destination.destination_objects.values(
        'city'
    ).annotate(count=Count('city')).order_by('-count')
    serializer_class = DestinationCityCountSerializer


@permission_classes([IsAuthenticated])
class DestinationCityActivityListAPI(generics.ListAPIView):
    """
    API endpoint returns destinations and their associated activities.
    Queryset includes city and activities.
    """
    queryset = Destination.destination_objects.values(
        'city',
        'activity1',
        'activity2',
        'activity3',
        'activity4'
    ).order_by(
        'city'
    )
    serializer_class = DestinationCityActivitySerializer
