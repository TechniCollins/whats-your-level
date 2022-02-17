from django.urls import re_path
from .views import TwitterActivity

urlpatterns = [
    re_path('activity', TwitterActivity.as_view())
]
