from rest_framework import serializers
from .models import Transaction, Block, Peer, TemporaryTrans

class TransactionSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Transaction
        exclude=('block','id') 

class BlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Block
        fields='__all__'

class TempSerializer(serializers.ModelSerializer):

    class Meta:
        model=TemporaryTrans
        fields='__all__'

    
