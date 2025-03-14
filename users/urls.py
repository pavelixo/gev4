from django.urls import path
from .views import LoginView, RegisterView, TransferView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('transfer/', TransferView.as_view(), name='transfer-view')
]