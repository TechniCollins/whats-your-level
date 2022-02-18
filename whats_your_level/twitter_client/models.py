from django.db import models

class TwitterAuthKey(models.Model):
    user_id = models.CharField(max_length=100)
    access_key = models.CharField(max_length=400)
    access_secret = models.CharField(max_length=400)

    class Meta:
        db_table = "authkey"


class Level(models.Model):
    level = models.IntegerField()
    message = models.CharField(max_length=1000)
    # In future, have a playlist attribute.
    # Instead of referencing music in the DB, we'll get
    # a random song from the playlist (URL) on Soundcloud, Spotify etc.
    # playlist = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.level)

    class Meta:
        db_table = "level"


class Music(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="music_level")
    url = models.CharField(max_length=1000)
    artist_handle = models.CharField(max_length=40, null=True) # The Twitter handle of the artist.

    def __str__(self):
        return self.url

    class Meta:
        db_table = "music"


class Mention(models.Model):
    level = models.IntegerField()
    handle = models.CharField(max_length=40)
    tweet_date = models.DateTimeField() # in UTC (Dictated by USE_TZ=True in settings.py)

    def __str__(self):
        return self.handle

    class Meta:
        db_table = "mention"
