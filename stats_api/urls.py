from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from stats_api.views import *

router = routers.DefaultRouter()
router.register('teams', TeamViewSet)
router.register('players', PlayerViewSet)
router.register('matches', MatchViewSet)
# router.register('transfers', TransferViewSet)
# router.register('popularities', PopularitiesViewSet)
router.register('player_match_stats', PlayerMatchStatsListView)
router.register('team_match_stats', TeamMatchStatsListView)
router.register('team_tournament_stats', TeamTournamentStatsView)
router.register('goals', GoalListView)

urlpatterns = [
    path('', include(router.urls)),
    path('add_player_match_stats/', CreatePlayerMatchStatsView.as_view()),
    path('add_team_match_stats/', CreateTeamMatchStatsView.as_view()),
]
