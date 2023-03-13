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


class GoalFilter(FilterSet):
    class Meta:
        model = Goal
        fields = {'scorer': ['exact'],
                  'match': ['exact'],
                  'assist_by': ['exact'],
                  'team': ['exact'],
                  'body_area': ['exact'],
                  'is_og': ['exact'],
                  'goal_type': ['exact'],
                  'time': ['gt', 'lt']}
