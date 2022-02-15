# Generated by Django 4.0.2 on 2022-02-15 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('message', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'level',
            },
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=40)),
                ('tweet_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'mention',
            },
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1000)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_level', to='twitter_client.level')),
            ],
            options={
                'db_table': 'music',
            },
        ),
    ]
