from django.shortcuts import render,redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from rest_framework import generics 
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import Transaction, Block, Peer, TemporaryTrans
from .serializers import TransactionSerializer, BlockSerializer, TempSerializer

class TransactionView(PermissionRequiredMixin, generics.ListCreateAPIView):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer
    permission_required=('core.add_transaction','core.view_transaction')
 
    def dispatch (self, request,*args, **kwargs):
        if request.method=="GET" and request.user.is_authenticated:
            self.queryset=Transaction.objects.filter(sender__user=request.user)
        return super().dispatch(request, *args, **kwargs)

class BlockView(PermissionRequiredMixin, generics.ListAPIView):
    queryset=Block.objects.all()
    serializer_class=BlockSerializer
    permission_required=('core.add_block','core.view_block')

    def dispatch (self, request,*args, **kwargs):
        if request.method=="GET" and request.user.is_authenticated:
            TEMP = getattr(settings, 'TEMP', [])
            print (TEMP)
        return super().dispatch(request, *args, **kwargs)

class TempView(PermissionRequiredMixin, generics.RetrieveUpdateAPIView):
    lookup_field='id'
    queryset=TemporaryTrans.objects.all()
    serializer_class=TempSerializer
    permission_required=('core.add_block','core.view_block')

    def dispatch (self, request,*args, **kwargs):
        # if request.method=="PUT" and request.user.is_authenticated:
        #     pass
        return super().dispatch(request, *args, **kwargs)
