from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import Team, Popularities, Transfer, Player


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


class TransferInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'player', 'former_club', 'cost')


class TransferOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'player', 'destination_club', 'cost')


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerMiniSerializer(many=True)
    in_transfers = TransferInSerializer(many=True)
    out_transfers = TransferOutSerializer(many=True)

    class Meta:
        model = Team
        fields = (
            'id', 'name', 'league', 'desc', 'president', 'get_value', 'avg_age', 'open_transfer_window', 'logo',
            'no_of_scores', 'avg_score', 'players', 'in_transfers', 'out_transfers')


class PopularitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popularities
        fields = ('id', 'team', 'user', 'popularity')
