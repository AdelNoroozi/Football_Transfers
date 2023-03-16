from django.shortcuts import render
from rest_framework import viewsets

from stats_api.serializers import TransferSerializer
from transfer.models import Transfer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    # permission_classes = (IsAdminUser,)