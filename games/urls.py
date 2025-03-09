from django.urls import path
from .views import MineView, MineAPIView

urlpatterns = [
    path('games/mine/', MineView.as_view(), name='mine-view'),
    path('api/games/mine/', MineAPIView.as_view(), name='mine-api-view')
]