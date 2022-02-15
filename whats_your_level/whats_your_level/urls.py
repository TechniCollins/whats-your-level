from django.urls import path, re_path, include

urlpatterns = [
    re_path(r'^api/', include('twitter_client.routers'))
]
