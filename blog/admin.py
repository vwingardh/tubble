from django.contrib import admin
from . import models


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'author',
        'status',
        'featured', 
        'created', 
    )
    prepopulated_fields = {'slug': ('title',), }
    

@admin.register(models.BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = (
        'blog', 
        'comment'
    )
