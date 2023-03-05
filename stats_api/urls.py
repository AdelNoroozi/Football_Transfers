from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from stats_api.views import TeamViewSet, TransferViewSet, PlayerViewSet, PopularitiesViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('teams', TeamViewSet)
router.register('players', PlayerViewSet)
router.register('transfers', TransferViewSet)
router.register('popularities', PopularitiesViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
