# Generated by Django 4.0.2 on 2022-02-17 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_client', '0005_twitterauth'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TwitterAuth',
            new_name='TwitterAuthKey',
        ),
    ]
