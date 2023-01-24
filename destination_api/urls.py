from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('destination-list/', views.DestinationCityCountryListAPI.as_view(), name='destination_list'),
    path('destination-count/', views.DestinationCityCountListAPI.as_view(), name='destination_count'),
    path('destination-activity/', views.DestinationCityActivityListAPI.as_view(), name='destination_activity_list'),
]
