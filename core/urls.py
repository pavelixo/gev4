from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from pages.views import (
    RootView,
    LoginView,
    RegisterView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('', RootView.as_view(), name='root-view')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)