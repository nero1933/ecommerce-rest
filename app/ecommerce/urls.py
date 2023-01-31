from django.urls import path, include

from .views import *


urlpatterns = [
    path('api/v1/hello-view', HelloAPIView.as_view(), name='hello-view'),
]