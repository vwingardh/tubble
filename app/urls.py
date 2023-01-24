from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('features/', views.features, name='features'),
    path('pricing/', views.pricing, name='pricing'),
    path('preview/', views.preview, name='preview'),
    path('about/', views.about_tubble, name='about_tubble'),
    path('careers/', views.careers, name='careers'),
    path('download/', views.mobile_app, name='mobile_app'),
    path('contact/', views.contact, name='contact'),
]
