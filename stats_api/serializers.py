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
        fields = ('id', 'name', 'league', 'logo',)


class PlayerSerializer(serializers.ModelSerializer):
    team = TeamMiniSerializer(many=False)

    class Meta:
        model = Player
        fields = (
            'id', 'name', 'nationality', 'desc', 'main_foot', 'age', 'market_value', 'team', 'post', 'picture')


class PlayerMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'picture', 'age', 'post')


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'player', 'former_club', 'destination_club', 'date', 'cost')


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            'id', 'host_team', 'host_team_goal_count', 'guest_team', 'guest_team_goal_count', 'time',
            'tournament_season',
            'status', 'round', 'stadium', 'main_referee', 'assist_referees')


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
    team = serializers.CharField(source='team.name')

    class Meta:
        model = TeamMatchStats
        fields = (
            'id', 'team', 'possession', 'corners', 'offsides', 'shots', 'shots_on_target', 'shot_percentage', 'goals',
            'complete_pass_percentage')


class MatchStatsSerializer(serializers.ModelSerializer):
    team_match_stats = TeamMatchStatsSerializer(many=True)

    class Meta:
        model = Match
        fields = (
            'id', 'host_team', 'host_team_goal_count', 'team_match_stats')


class PlayerMatchStatsSerializer(serializers.ModelSerializer):
    player = serializers.CharField(source='player.name')

    class Meta:
        model = PlayerMatchStats
        fields = (
            'id', 'player')


class TransferInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'player', 'former_club', 'cost')


class TransferOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'player', 'destination_club', 'cost')


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerMiniSerializer(many=True, required=False)
    in_transfers = TransferInSerializer(many=True, required=False)
    out_transfers = TransferOutSerializer(many=True, required=False)

    class Meta:
        model = Team
        fields = (
            'id', 'name', 'league', 'desc', 'president', 'get_value', 'avg_age', 'open_transfer_window', 'logo',
            'no_of_scores', 'avg_score', 'players', 'in_transfers', 'out_transfers')


class PopularitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popularities
        fields = ('id', 'team', 'popularity')
