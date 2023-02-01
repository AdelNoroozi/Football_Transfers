from rest_framework import serializers

from api.models import Team, Popularities, Transfer, Player


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'league', 'desc', 'president', 'market_value', 'open_transfer_window', 'logo', 'no_of_scores', 'avg_score')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'name', 'nationality', 'desc', 'main_foot', 'age', 'team', 'post', 'picture')


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'player', 'former_club', 'destination_club', 'date', 'cost')


class PopularitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popularities
        fields = ('id', 'team', 'user', 'popularity')
