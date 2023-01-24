from django.contrib import admin
from . import models


@admin.register(models.Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'has_user_visited',
        'city', 
        'country', 
        'slug' 
    )
    prepopulated_fields = {'slug': ('city',), }
