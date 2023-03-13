from django_filters.rest_framework import FilterSet
from .models import *


class PlayerMatchStatsFilter(FilterSet):
    class Meta:
        model = PlayerMatchStats
        fields = {'player': ['exact'],
                  'players_team': ['exact'],
                  'match': ['exact']}


class TeamMatchStatsFilter(FilterSet):
    class Meta:
        model = TeamMatchStats
        fields = {'team': ['exact'],
                  'match': ['exact']}
