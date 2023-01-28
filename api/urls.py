from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import TeamViewSet, TransferViewSet, PlayerViewSet, PopularitiesViewSet

router = routers.DefaultRouter()
router.register('teams', TeamViewSet)
router.register('players', PlayerViewSet)
router.register('transfers', TransferViewSet)
router.register('popularities', PopularitiesViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
