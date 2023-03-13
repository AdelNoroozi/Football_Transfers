from django.contrib.auth.models import User
from rest_framework import viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAdminUser, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from ai.algorithms import calculater_player_score
from stats_api.filters import PlayerMatchStatsFilter
from stats_api.models import Team, Player, Transfer, Popularities, Match
from stats_api.serializers import *


#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (AllowAny,)

    # detail true means the methods will apply on a single team, else it will apply on the whole list
    @action(detail=True, methods=['POST'])
    def save_fan_score(self, request, pk=None):
        if 'in_score' in request.data:
            team = Team.objects.get(id=pk)
            in_score = request.data['in_score']
            user = request.user
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


# class CustomPermissionClass(BasePermission):
#     def has_permission(self, request, view):
#         if request.method == 'GET':
#             return True
#         elif request.method == 'POST':
#             return bool(request.user and request.user.is_staff)


class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    @action(detail=True, methods=['GET'])
    def event_line(self, request, pk=None):
        try:
            match = Match.objects.get(id=pk)
        except:
            response = {'message': 'match_not_found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MatchEventsSerializer(match)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def stats(self, request, pk=None):
        try:
            match = Match.objects.get(id=pk)
        except:
            response = {'message': 'match_not_found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = MatchStatsSerializer(match)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def submit_match_goals(self, request, pk=None):
        try:
            match = Match.objects.get(id=pk)
        except:
            response = {'message': 'match_not_found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                scorer_id = request.data['scorer_id']
                assistant_id = request.data['assistant_id']
            except:
                response = {'message': 'invalid fields or data'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    scorer = Player.objects.get(id=scorer_id)
                    assistant = Player.objects.get(id=assistant_id)
                except:
                    response = {'scorer or assistant player not found'}
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                else:
                    try:
                        time = request.data['time']
                        body_area = request.data['body_area']
                        is_og = request.data['is_og']
                    except:
                        response = {'message': 'invalid fields or data'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if is_og == 'True':
                            scorers_team = scorer.team
                            if scorers_team == match.host_team:
                                team = match.guest_team
                            else:
                                team = match.host_team
                        elif is_og == 'False':
                            team = scorer.team
                        else:
                            response = {'message': 'invalid fields or data'}
                            return Response(response, status=status.HTTP_400_BAD_REQUEST)
                        goal = Goal.objects.create(match=match, scorer=scorer, assist_by=assistant, team=team,
                                                   time=time,
                                                   body_area=body_area, is_og=is_og)
                        serializer = GoalSerializer(goal)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def submit_match_bookings(self, request, pk=None):
        try:
            match = Match.objects.get(id=pk)
        except:
            response = {'message': 'match_not_found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                player_id = request.data['player_id']
            except:
                response = {'message': 'invalid fields or data'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    player = Player.objects.get(id=player_id)
                except:
                    response = {'player not found'}
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                else:
                    try:
                        time = request.data['time']
                        card = request.data['card']
                    except:
                        response = {'message': 'invalid fields or data'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        booking = Booking.objects.create(player=player, match=match, team=player.team, time=time,
                                                         card=card)
                        serializer = BookingEventSerializer(booking)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'])
    def submit_match_substitutions(self, request, pk=None):
        try:
            match = Match.objects.get(id=pk)
        except:
            response = {'message': 'match_not_found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                in_player_id = request.data['in_player_id']
                out_player_id = request.data['out_player_id']
            except:
                response = {'message': 'invalid fields or data'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    in_player = Player.objects.get(id=in_player_id)
                    out_player = Player.objects.get(id=out_player_id)
                except:
                    response = {'player not found'}
                    return Response(response, status=status.HTTP_404_NOT_FOUND)
                else:
                    try:
                        time = request.data['time']
                    except:
                        response = {'message': 'invalid fields or data'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        sub = Substitution.objects.create(match=match, in_player=in_player, out_player=out_player,
                                                          team=in_player.team, time=time)
                        serializer = SubEventSerializer(sub)
                        return Response(serializer.data, status= status.HTTP_201_CREATED)


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (CustomPermissionClass,)

    @action(detail=True, methods=['POST'], )
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


class CreatePlayerMatchStatsView(APIView):

    def post(self, request):
        player_id = request.data['player_id']
        match_id = request.data['match_id']
        try:
            player = Player.objects.get(id=player_id)
            match = Match.objects.get(id=match_id)
        except:
            response = {'match or player not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                saves = int(request.data['saves'])
                passes = int(request.data['passes'])
                complete_passes = int(request.data['complete_passes'])
                dribbles = int(request.data['dribbles'])
                blocks = int(request.data['blocks'])
                interceptions = int(request.data['interceptions'])
                key_passes = int(request.data['key_passes'])
                shots = int(request.data['shots'])
                shots_on_target = int(request.data['shots_on_target'])
                chances_missed = int(request.data['chances_missed'])
                post_hits = int(request.data['post_hits'])
            except:
                response = {'message': 'invalid fields or data'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                shot_percentage = int((shots_on_target / shots) * 100)
                complete_pass_percentage = int((complete_passes / passes) * 100)
                own_goals = Goal.objects.filter(is_og=True, match=match, scorer=player).count()
                goals = Goal.objects.filter(is_og=False, match=match, scorer=player).count()
                assists = Goal.objects.filter(is_og=False, match=match, assist_by=player).count()
                yellow_cards = Booking.objects.filter(card='Y', match=match, player=player).count()
                red_cards = Booking.objects.filter(card='R', match=match, player=player).count()
                score = calculater_player_score(player, saves, passes, complete_passes, dribbles, blocks, interceptions,
                                                key_passes,
                                                shots_on_target, chances_missed, post_hits, goals, own_goals, assists,
                                                yellow_cards,
                                                red_cards)
                try:
                    PlayerMatchStats.objects.get(player=player, match=match)
                except:
                    if shots_on_target > shots or post_hits > shots:
                        response = {'shots on target or post hits can not be more than shots'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    if complete_passes > passes:
                        response = {'complete passes can not be more than passes'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                    player_match_stats = PlayerMatchStats.objects.create(player=player, match=match,
                                                                         players_team=player.team,
                                                                         saves=saves,
                                                                         passes=passes, complete_passes=complete_passes,
                                                                         dribbles=dribbles,
                                                                         blocks=blocks, interceptions=interceptions,
                                                                         key_passes=key_passes, shots=shots,
                                                                         shots_on_target=shots_on_target,
                                                                         chances_missed=chances_missed,
                                                                         post_hits=post_hits,
                                                                         shot_percentage=shot_percentage,
                                                                         complete_pass_percentage=complete_pass_percentage,
                                                                         own_goals=own_goals, goals=goals,
                                                                         assists=assists,
                                                                         yellow_cards=yellow_cards,
                                                                         red_cards=red_cards, score=score
                                                                         )
                    serializer = PlayerMatchStatsSerializer(player_match_stats)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    response = {'stats already exist'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PlayerMatchStatsListView(mixins.ListModelMixin,
                               GenericViewSet):
    queryset = PlayerMatchStats.objects.all()
    serializer_class = PlayerMatchStatsMiniSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PlayerMatchStatsFilter
    ordering_fields = ['saves', 'passes', 'complete_passes', 'complete_pass_percentage',
                       'dribbles', 'blocks',
                       'interceptions', 'key_passes', 'shots', 'shots_on_target', 'shot_percentage', 'post_hits',
                       'chances_missed',
                       'own_goals', 'goals',
                       'assists', 'yellow_cards', 'red_cards', 'score']


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    # permission_classes = (IsAdminUser,)


class PopularitiesViewSet(viewsets.ModelViewSet):
    queryset = Popularities.objects.all()
    serializer_class = PopularitiesSerializer
    authentication_classes = (TokenAuthentication,)

    # permission_classes = (IsAdminUser,)

    def update(self, request, *args, **kwargs):
        response = {'message': 'cant update inside relation'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'cant create inside relation'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
