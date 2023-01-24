from django.urls import path
from . import views


app_name = 'workspace'

urlpatterns = [
    path('', views.workspace_home, name='workspace_home'),
    path('create-destination/', views.create_destination, name='create_destination'),
    path('details/<str:slug>/', views.destination_detail_view, name='destination_detail_view'),
    path('update/<int:pk>', views.update_destination, name='update_destination'),
    path('delete/<int:pk>/', views.delete_destination, name='delete_destination'),
    path('list-destinations/', views.list_destinations, name='list_destinations'),
    path('list-destinations/filter/<str:filter>/', views.filter_destinations, name='filter_destinations'),
    path('list-destinations/sort/<str:sort>/', views.sort_destinations, name='sort_destinations'),
    path('list-visited/', views.list_visited_destinations, name='list_visited_destinations'),
    path('list-visited/filter/<str:filter>/', views.filter_visited_destinations, name='filter_visited_destinations'),
    path('list-visited/sort/<str:sort>/', views.sort_visited_destinations, name='sort_visited_destinations'),
    path('filter-next-adventure/', views.filter_next_adventure, name='filter_next_adventure'),
    path('api-home/', views.api_home, name='api_home'),
]
