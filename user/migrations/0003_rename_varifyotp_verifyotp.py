# Generated by Django 4.2.4 on 2023-08-28 17:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0002_alter_userinfo_role_varifyotp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VarifyOtp',
            new_name='VerifyOtp',
        ),
    ]
