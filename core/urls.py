from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from pages.urls import urlpatterns as page_patterns
from users.urls import urlpatterns as user_patterns
from games.urls import urlpatterns as game_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
] 

urlpatterns += page_patterns
urlpatterns += user_patterns
urlpatterns += game_patterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)