# Generated by Django 4.0.2 on 2022-02-16 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_client', '0003_alter_mention_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='artist_handle',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
