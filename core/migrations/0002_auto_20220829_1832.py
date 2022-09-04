from django.db import migrations


class Migration(migrations.Migration):

    def create_groups(apps, schema_migration):
        User=apps.get_model('auth', 'User')
        Group=apps.get_model('auth','Group')
        Permission=apps.get_model('auth','Permission')
        Peer=apps.get_model('core','Peer')
        Validator=apps.get_model('core','Validator')

        add_transaction=Permission.objects.get(codename='add_transaction')
        add_block=Permission.objects.get(codename='add_block')

        peers_permissions=[
            add_transaction
        ]

        validators_permissions=[
            add_block
        ]

        peers_group=Group(name='Peers')
        peers_group.save()
        peers_group.permissions.set(peers_permissions)

        validators_group=Group(name='Validators')
        validators_group.save()
        validators_group.permissions.set(validators_permissions)

        for user in User.objects.all():
            if Peer.objects.filter(user=user):
                peers_group.user_set.add(user)

        for user in User.objects.all():
            if Validator.objects.filter(user=user):
                validators_group.user_set.add(user)


    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_groups)
    ]

