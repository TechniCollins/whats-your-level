# Generated by Django 4.0.2 on 2022-02-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mention',
            name='level',
            field=models.CharField(default='8', max_length=40),
            preserve_default=False,
        ),
    ]