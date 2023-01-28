from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from api.models import Team, Player, Transfer, Popularities
from api.serializers import TeamSerializer, PlayerSerializer, TransferSerializer, PopularitiesSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class PopularitiesViewSet(viewsets.ModelViewSet):
    queryset = Popularities.objects.all()
    serializer_class = PopularitiesSerializer
