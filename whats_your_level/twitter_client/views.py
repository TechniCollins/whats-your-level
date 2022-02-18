from rest_framework.views import APIView
from datetime import datetime
from django.utils import timezone
from random import randint

# for API responses
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status

from .models import Mention, Music, TwitterAuthKey

import re

from django.conf import settings

# Interact with the twitter API
import tweepy
from .management.commands.extended_tweepy import API

# Webhook app verification
import base64
import hashlib
import hmac


class TwitterAuth(APIView):
    auth = tweepy.OAuthHandler(
        settings.CONSUMER_KEY,
        settings.CONSUMER_SECRET,
        settings.CALLBACK_URL
    )

    def get(self, request):
        auth = self.auth

        if "authenticate" in request.GET:
            # Get redirect URL
            try:
                redirect_url = auth.get_authorization_url()
                return Response({"url": redirect_url}, status.HTTP_200_OK)
            except tweepy.TweepyException as e:
                return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.GET.get("oauth_token"):
            try:
                auth_token = request.GET['oauth_token']
                verifier = request.GET['oauth_verifier']

                auth.request_token = {'oauth_token': auth_token, 'oauth_token_secret': verifier}

                access_keys = auth.get_access_token(verifier)

                # Get user id and save credentials
                TwitterAuthKey.objects.all().delete()
                auth_instance = TwitterAuthKey(
                    access_key=access_keys[0],
                    access_secret=access_keys[1]
                )

                auth.set_access_token(auth_instance.access_key, auth_instance.access_secret)
                user_details = API(auth, wait_on_rate_limit=True).verify_credentials()                
                auth_instance.user_id = str(user_details.id)
                auth_instance.save()


                # Subscribe to this user's activity
                subscription = API(auth, wait_on_rate_limit=True).subscribeToUser()
                print(subscription)

                return Response({"message": "Subscribed to user"}, status.HTTP_200_OK)
            except Exception as e:
                return Response({"message": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                user_id = tweet.get("user").get("id_str")

                twitter_auth = TwitterAuthKey.objects.all()[0]

                if user_id == twitter_auth.user_id:
                    print("User mentioned self. Avoiding tweet")
                    return Response({"message": "Self mention"}, status.HTTP_200_OK)

                tweet_id = tweet.get("id")
                text = tweet.get("text")
                username = tweet.get("user").get("screen_name")
                tweet_date = datetime.strptime(tweet.get('created_at'), "%a %b %d %H:%M:%S %z %Y").replace(tzinfo=timezone.utc)

                level = re.search(r"10|[1-9]", text)

                if not level:
                    return Response({"message": "No Level"}, status.HTTP_200_OK)

                level = int(level.group(0))

                # Get at most 3 people who tweeted the same level today
                tags = Mention.objects.filter(
                        level=level,
                        tweet_date__gte=timezone.now().replace(hour=0, minute=0, second=0),
                        tweet_date__lte=timezone.now().replace(hour=23, minute=59, second=59)
                ).exclude(handle=username).order_by("-id") # .distinct("handle")[:3]

                # order by and distinct don't go well together and won't work in our case;
                # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#django.db.models.query.QuerySet.distinct
                # so we'll have to eliminate duplicates using python code. Python sets won't work either because
                # they won't maintain order (which we need to avoid mentioning the same 3 users throughout the day)
                # For now, we'll get all users who tweeted within the day. As long as this number is in the hundreds,
                # performance won't be an issue. Response will still be sent within a second or two
                mentions = list(dict.fromkeys([f"@{x.handle}, " for x in tags]))[:3] #https://stackoverflow.com/a/17016257/9366954

                # Get music for the given level
                music = Music.objects.filter(level__level=level).prefetch_related("level")

                if not music:
                    return Response({"message": "No Music"}, status.HTTP_200_OK)

                # Get a random url from the results.
                # Well use len instead of .count() to avoid making an extra query
                n = len(music)
                message = music[randint(0,n-1)]

                # Check number of mentions at level x
                m = len(mentions)

                tag_text = ""

                if m:
                    tag_text = tag_text.join(mentions)

                if tag_text != "" and m==1:
                    tag_text = f"Also meet {tag_text} who was at {message.level.level} today."
                elif tag_text != "" and m > 1:
                    tag_text = f"Also meet {tag_text} who were at {message.level.level} today."
                
                tweet_text = f"{re.sub('username', f'@{username}', message.level.message)}\n{message.url}"
                
                if tag_text != "":
                    tweet_text += f"\n\n{tag_text}"

                print(tweet_text)

                # Post tweet
                auth = tweepy.OAuth1UserHandler(
                    settings.CONSUMER_KEY, settings.CONSUMER_SECRET,
                    twitter_auth.access_key, twitter_auth.access_secret
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
