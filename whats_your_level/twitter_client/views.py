from rest_framework.views import APIView
from datetime import datetime
from django.utils import timezone
from random import randint

# for API responses
from rest_framework.response import Response
from rest_framework import status

from .models import Mention, Music

import re


class TwitterActivity(APIView):
    def get(self, request):
        return

    def post(self, request):
        data = request.data

        # HANDLE MENTIONS
        # We know it's a mention if it has the 'user_has_blocked' attribute
        if data.get("user_has_blocked") is not None:
            for tweet in data.get("tweet_create_events"):
                text = tweet.get("text")
                username = tweet.get("user").get("screen_name")
                tweet_date = datetime.strptime(tweet.get('created_at'), "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

                level = re.search(r"[0-9]", text)

                if not level:
                    return Response({"message": "No Level"}, status.HTTP_200_OK)

                level = int(level.group(0))

                # Get at most 3 people who tweeted the same level today
                tags = Mention.objects.filter(
                    level=level,
                    tweet_date__gte=timezone.now().replace(hour=0, minute=0, second=0),
                    tweet_date__lte=timezone.now().replace(hour=23, minute=59, second=59)
                ).exclude(handle=username)[:3]

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
                    tag_text = tag_text.join([f", @{x.handle}" for x in tags])

                if tag_text != "" and m==1:
                    tag_text = f"Also meet {tag_text} who was at {message.level.level} today."
                elif tag_text != "" and m > 1:
                    tag_text = f"Also meet {tag_text} who were at {message.level.level} today." 
                else:
                    tag_text = f"You're the first one at {message.level.level} today"
                
                tweet_text = f"@{username} {message.level.message}\n{message.url}\n{tag_text}"

                Mention(
                    level=level,
                    handle=username,
                    tweet_date=tweet_date
                ).save()

                print(tweet_text)

        return Response({"message": tweet_text}, status.HTTP_200_OK)
