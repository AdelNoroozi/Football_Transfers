from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from stats_api.views import *

router = routers.DefaultRouter()
router.register('teams', TeamViewSet)
router.register('players', PlayerViewSet)
router.register('matches', MatchViewSet)
router.register('transfers', TransferViewSet)
router.register('popularities', PopularitiesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add_player_match_stats/', CreatePlayerMatchStatsView.as_view())
]
