from rest_framework.views import APIView
from datetime import datetime
from django.utils import timezone
from random import randint

# for API responses
from rest_framework.response import Response
from rest_framework import status

from .models import Mention, Music

import re

from django.conf import settings

# Interact with the twitter API
import tweepy
from .management.commands.extended_tweepy import API

# Webhook app verification
import base64
import hashlib
import hmac


class TwitterActivity(APIView):
    def get(self, request):
        # creates HMAC SHA-256 hash from incomming token and your consumer secret
        sha256_hash_digest = hmac.new(
            key=bytes(settings.CONSUMER_SECRET, 'utf-8'),
            msg=bytes(request.GET.get('crc_token'), 'utf-8'),
            digestmod=hashlib.sha256
        ).digest()

        # construct response data with base64 encoded hash
        response = {
            'response_token': 'sha256=' + base64.b64encode(sha256_hash_digest).decode('ascii')
        }

        return Response(response, status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # HANDLE MENTIONS
        # We know it's a mention if it has the 'user_has_blocked' attribute
        tweet_text = ""

        if data.get("user_has_blocked") is not None:
            for tweet in data.get("tweet_create_events"):
                tweet_id = tweet.get("id")
                text = tweet.get("text")
                username = tweet.get("user").get("screen_name")
                tweet_date = datetime.strptime(tweet.get('created_at'), "%a %b %d %H:%M:%S %z %Y").replace(tzinfo=timezone.utc)

                level = re.search(r"10|[1-9]", text)

                if not level:
                    return Response({"message": "No Level"}, status.HTTP_200_OK)

                level = int(level.group(0))

                # Get at most 3 people who tweeted the same level today
                tags = list(
                    Mention.objects.filter(
                        level=level,
                        tweet_date__gte=timezone.now().replace(hour=0, minute=0, second=0),
                        tweet_date__lte=timezone.now().replace(hour=23, minute=59, second=59)
                    ).exclude(handle=username).values_list("handle", flat=True).distinct()[:3]
                )

                # Get music for the given level
                music = Music.objects.filter(level__level=level).prefetch_related("level")

                if not music:
                    return Response({"message": "No Music"}, status.HTTP_200_OK)

                # Get a random url from the results.
                # Well use len instead of .count() to avoid making an extra query
                n = len(music)
                message = music[randint(0,n-1)]

                # Check number of mentions at level x
                m = len(tags)

                tag_text = ""

                if m:
                    tag_text = tag_text.join([f"@{x}, " for x in tags])

                if tag_text != "" and m==1:
                    tag_text = f"Also meet {tag_text} who was at {message.level.level} today."
                elif tag_text != "" and m > 1:
                    tag_text = f"Also meet {tag_text} who were at {message.level.level} today." 
                else:
                    tag_text = f"You're the first one at {message.level.level} today"
                
                tweet_text = f"{re.sub('username', f'@{username}', message.level.message)}\n{message.url}"

                # Mention artist if handle is available
                if message.artist_handle:
                    tweet_text += f" via @{message.artist_handle}"

                tweet_text += f"\n\n{tag_text}"

                # Post tweet
                auth = tweepy.OAuth1UserHandler(
                    settings.CONSUMER_KEY, settings.CONSUMER_SECRET,
                    settings.ACCESS_TOKEN, settings.ACCESS_SECRET
                )

                API(auth).update_status(
                    status=tweet_text,
                    in_reply_to_status_id=tweet_id
                )

                Mention(
                    level=level,
                    handle=username,
                    tweet_date=tweet_date
                ).save()

        return Response({"message": tweet_text}, status.HTTP_200_OK)
