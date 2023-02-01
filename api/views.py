from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Team, Player, Transfer, Popularities
from api.serializers import TeamSerializer, PlayerSerializer, TransferSerializer, PopularitiesSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    # detail true means the methods will apply on a single team, else it will apply on the whole list
    @action(detail=True, methods=['POST'])
    def save_fan_score(self, request, pk=None):
        if 'in_score' in request.data:
            team = Team.objects.get(id=pk)
            in_score = request.data['in_score']
            user = User.objects.get(id=1)
            try:
                score = Popularities.objects.get(user=user.id, team=team.id)
                score.popularity = in_score
                score.save()
                serializer = PopularitiesSerializer(score, many=False)
                response = {'score updated successfully'}
                return Response(response, status=status.HTTP_200_OK)
            except:
                score = Popularities.objects.create(user=user, team=team, popularity=in_score)
                serializer = PopularitiesSerializer(score, many=False)
                response = {'score created successfully'}
                return Response(response, status=status.HTTP_200_OK)


        else:
            response = {'no score received'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=True, methods=['POST'])
    def transfer(self, request, pk=None):
        try:
            player = Player.objects.get(id=pk)
            dest_team = request.data['dest_team']
            date = request.data['date']
            cost = request.data['cost']
            transfer = Transfer.objects.create(player=player, former_club=player.team, destination_club_id=dest_team,
                                               date=date, cost=cost)
            serializer = TransferSerializer(transfer, many=False)
            player.team = Team.objects.get(id=dest_team)
            player.save()
            response = {'transfer created successfully'}
            return Response(response, status=status.HTTP_200_OK)
        except:
            response = {'bad data'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class PopularitiesViewSet(viewsets.ModelViewSet):
    queryset = Popularities.objects.all()
    serializer_class = PopularitiesSerializer
