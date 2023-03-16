from rest_framework import serializers
from transfer.models import Transfer


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
