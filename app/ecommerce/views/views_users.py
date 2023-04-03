from django.db import IntegrityError
from django.http import Http404

from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView

from app import settings
from ..models import UserProfile
from ..serializers.serializers_password_reset import PasswordResetSerializer, PasswordResetConfirmSerializer
from ..serializers.serializers_users import RegistrationSerializer, PasswordChangeSerializer
from ..utils.email.send import EmailRegister, EmailPasswordReset
from ..utils.email.verify import PasswordResetConfirm, RegisterConfirm


class RegisterAPIView(CreateAPIView, EmailRegister):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        try:
            serializer.save()
        except IntegrityError:
            return Response("Email already exists.",
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        user_id = serializer.data['id']
        user = get_object_or_404(UserProfile, id=user_id)
        self.email_register(request, user) # method from EmailRegister
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RegisterConfirmAPIView(APIView, RegisterConfirm):

    def get(self, request, token):
        return self.register_confirm(token) # method from ConfirmRegister


class PasswordResetAPIView(APIView, EmailPasswordReset):

    def post(self, request):
        serializer = PasswordResetSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = get_object_or_404(UserProfile, email=email)
            self.email_password_reset(request, user)
            return Response({'message': 'Email send. Check your mailbox'}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class PasswordResetConfirmAPIView(APIView, PasswordResetConfirm):

    def post(self, request, token):
        serializer = PasswordResetConfirmSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        return self.password_reset_confirm(new_password, token) # method from PasswordResetConfirm


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
