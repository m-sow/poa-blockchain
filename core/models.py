from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group,User,Permission
from django.contrib.contenttypes.models import ContentType

from django.conf import settings

class Peer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Validator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation=models.DecimalField(default=0,max_digits=5, decimal_places=2)

    def __str__(self):
        return self.user.username

class Block(models.Model):
    previous_hash=models.CharField(max_length=255)
    current_hash=models.CharField(max_length=255)
    validated_by=models.ForeignKey(Validator, on_delete=models.CASCADE)
    date_time=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  "Block n° "+ str(self.id)

class Transaction(models.Model):
    sender=models.ForeignKey(Peer, on_delete=models.CASCADE, related_name="peer")
    content=models.TextField()
    block=models.ForeignKey(Block, on_delete=models.CASCADE, null=True, blank=True)
    date_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['date_time']

    def __str__(self):
        return "Transaction n° "+ str(self.id)


class TemporaryTrans(models.Model):
    to_be_validated_by=models.ForeignKey(Validator, null=True, on_delete=models.CASCADE)
    trans=models.ManyToManyField(Transaction)



@receiver(post_save, sender=Validator)
def set_group(sender,instance,**kwargs):
    validators_group, created=Group.objects.get_or_create(name="Validators")
    
    content_type=ContentType.objects.get_for_model(Block)
    block_permissions=Permission.objects.filter(content_type=content_type)
    
    validators_group.permissions.set(block_permissions)
    validators_group.user_set.add(instance.user)


@receiver(post_save, sender=Peer)
def set_group(sender,instance,**kwargs):
    peers_group, created=Group.objects.get_or_create(name="Peers")
    
    content_type=ContentType.objects.get_for_model(Transaction)
    transaction_permissions=Permission.objects.filter(content_type=content_type)
    
    peers_group.permissions.set(transaction_permissions)
    peers_group.user_set.add(instance.user)
     

@receiver(post_save, sender=Transaction)
def check_validator(sender,instance,**kwargs):
    validator=Validator.objects.get(id=1)
    temp_trans, __=TemporaryTrans.objects.get_or_create(to_be_validated_by=validator)
    temp_trans.trans.add(instance)

    # print(validator)
    # print(temp_trans)

    # TEMP = getattr(settings, 'TEMP', [])
    # TEMP.append(instance)
    # print (TEMP)


         




