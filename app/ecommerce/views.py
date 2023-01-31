from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response


class HelloAPIView(APIView):
    """ Test APIView. """

    def get(self, request, format=None):
        an_apiview = [
            'list',
            'to test',
            'api',
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})
