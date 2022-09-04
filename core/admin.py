from django.contrib import admin
from .models import Transaction, TemporaryTrans
from .models import Block
from .models import Peer
from .models import Validator


admin.site.register(Transaction)
admin.site.register(Block)
admin.site.register(Peer)
admin.site.register(Validator)
admin.site.register(TemporaryTrans)

