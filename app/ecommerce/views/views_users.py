import uuid
import datetime

from django.core.cache import cache

from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import IntegrityError
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from app import settings
from ..models import UserProfile
from ..serializers.serializers_users import RegistrationSerializer, PasswordChangeSerializer
from ..utils.email.send import EmailRegister
from ..utils.email.verify import ConfirmRegister


class RegistrationAPIView(CreateAPIView, EmailRegister):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            return Response("Email already exists.",
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        user_id = serializer.data['id']
        self.email_register(request, user_id) # method from EmailRegister
        return Response(status=status.HTTP_201_CREATED)


class ConfirmRegisterAPIView(APIView, ConfirmRegister):

    def get(self, request, token):
        self.confirm_register(token) # method from ConfirmRegister


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
