from django.urls import path, include

from .views import *


urlpatterns = [
    path('api/v1/products', ProductAPIList.as_view(), name='products'),
    path('api/v1/products/<slug:slug>', ProductAPIDetailView.as_view(), name='product'),
]
