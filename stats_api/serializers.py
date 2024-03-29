from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from stats_api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class TeamMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'logo',)


class PlayerSerializer(serializers.ModelSerializer):
    team = TeamMiniSerializer(many=False)

    class Meta:
        model = Player
        fields = (
            'id', 'name', 'nationality', 'desc', 'main_foot', 'team', 'post', 'picture')


class PlayerMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'picture', 'post')





class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            'id', 'host_team', 'host_team_goal_count', 'guest_team', 'guest_team_goal_count', 'time',
            'tournament_season',
            'status', 'round', 'stadium', 'main_referee', 'assist_referees')


class MatchMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            'id', 'id', 'host_team', 'guest_team', 'tournament_season', 'round'
        )


class GoalSerializer(serializers.ModelSerializer):
    scorer = PlayerMiniSerializer(many=False)
    team = TeamMiniSerializer(many=False)
    assist_by = PlayerMiniSerializer(many=False)

    class Meta:
        model = Goal
        fields = ('id', 'team', 'scorer', 'assist_by', 'time', 'body_area', 'is_og')


class GoalEventSerializer(serializers.ModelSerializer):
    scorer = serializers.CharField(source='scorer.name')
    team = serializers.CharField(source='team.name')

    class Meta:
        model = Goal
        fields = ('id', 'team', 'scorer', 'time', 'is_og')


class BookingEventSerializer(serializers.ModelSerializer):
    player = serializers.CharField(source='player.name')
    team = serializers.CharField(source='team.name')

    class Meta:
        model = Booking
        fields = ('id', 'team', 'player', 'time', 'card')


class SubEventSerializer(serializers.ModelSerializer):
    in_player = serializers.CharField(source='in_player.name')
    out_player = serializers.CharField(source='out_player.name')
    team = serializers.CharField(source='team.name')

    class Meta:
        model = Booking
        fields = ('id', 'team', 'in_player', 'out_player', 'time')


class MatchEventsSerializer(serializers.ModelSerializer):
    goals = GoalEventSerializer(many=True)
    bookings = BookingEventSerializer(many=True)
    subs = SubEventSerializer(many=True)

    class Meta:
        model = Match
        fields = (
            'id', 'host_team', 'host_team_goal_count', 'goals', 'bookings', 'subs')


class TeamMatchStatsSerializer(serializers.ModelSerializer):
    team = TeamMiniSerializer(many=False)
    match = MatchMiniSerializer(many=False)

    class Meta:
        model = TeamMatchStats
        fields = (
            'id', 'team', 'match', 'possession', 'corners', 'offsides', 'shots', 'shots_on_target', 'shot_percentage',
            'goals',
            'complete_pass_percentage')


class MatchStatsSerializer(serializers.ModelSerializer):
    team_match_stats = TeamMatchStatsSerializer(many=True)

    class Meta:
        model = Match
        fields = (
            'id', 'host_team', 'host_team_goal_count', 'team_match_stats')


class PlayerMatchStatsSerializer(serializers.ModelSerializer):
    player = PlayerMiniSerializer(many=False)
    players_team = TeamMiniSerializer(many=False)
    match = MatchMiniSerializer(many=False)

    class Meta:
        model = PlayerMatchStats
        fields = (
            'id', 'player', 'players_team', 'match', 'saves', 'passes', 'complete_passes', 'complete_pass_percentage',
            'dribbles', 'blocks',
            'interceptions', 'key_passes', 'shots', 'shots_on_target', 'shot_percentage', 'post_hits', 'chances_missed',
            'own_goals', 'goals',
            'assists', 'yellow_cards', 'red_cards', 'score')


class PlayerMatchStatsMiniSerializer(serializers.ModelSerializer):
    player = PlayerMiniSerializer(many=False)
    players_team = TeamMiniSerializer(many=False)
    match = MatchMiniSerializer(many=False)

    class Meta:
        model = PlayerMatchStats
        fields = (
            'id', 'player', 'players_team', 'match', 'score')


class TeamMatchStatsMiniSerializer(serializers.ModelSerializer):
    team = TeamMiniSerializer
    match = MatchMiniSerializer(many=False)

    class Meta:
        model = TeamMatchStats
        fields = (
            'id', 'team', 'match')


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerMiniSerializer(many=True, required=False)

    class Meta:
        model = Team
        fields = (
            'id', 'name', 'league', 'desc', 'president', 'get_value', 'avg_age', 'open_transfer_window', 'logo',
            'no_of_scores', 'avg_score', 'players')


class TournamentSeasonMiniSerializer(serializers.ModelSerializer):
    tournament = serializers.CharField(source='tournament.name')

    class Meta:
        model = TournamentSeason
        fields = ('id', 'tournament', 'season')


class TeamTournamentStatsSerializer(serializers.ModelSerializer):
    team = TeamMiniSerializer(many=False)
    tournament_season = TournamentSeasonMiniSerializer(many=False)

    class Meta:
        model = TeamTournamentStats
        fields = (
            'id', 'team', 'tournament_season', 'points', 'wins', 'loses', 'draws', 'goals_scored', 'goals_received')


class PopularitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popularity
        fields = ('id', 'team', 'popularity')
