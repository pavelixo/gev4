from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse

def debug(request):
    return HttpResponse(
        f'DEBUG: {settings.DEBUG}\n' +
        f'SECRET_KEY: {settings.SECRET_KEY}\n'
        f'DEFAULT: {settings.DATABASES["default"]}\n', 
        content_type='text/plain'
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('debug/', debug)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)