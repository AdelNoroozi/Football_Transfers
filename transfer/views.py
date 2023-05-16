from django.shortcuts import render
from rest_framework import viewsets

from transfer.models import Transfer
from transfer.serializers import TransferSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    # permission_classes = (IsAdminUser,)
