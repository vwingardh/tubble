from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls', namespace='app')),
    path('account/', include('account.urls', namespace='account')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('workspace/', include('workspace.urls', namespace='workspace')), 
    path('blog/', include('blog.urls', namespace='blog')), 
    path('api/', include('destination_api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    