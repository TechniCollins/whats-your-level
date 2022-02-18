from django.urls import path, re_path, include

from twitter_client.views import TwitterAuth

urlpatterns = [
    re_path(r'^api/', include('twitter_client.routers')),
    re_path(r'^twitter-auth/$', TwitterAuth.as_view(), name="twitter-auth")
]
