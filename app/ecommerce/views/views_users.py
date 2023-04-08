from django.db import IntegrityError

from rest_framework import status
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView

from ..models import UserProfile
from ..serializers.serializers_password_reset import PasswordResetSerializer, PasswordResetConfirmSerializer
from ..serializers.serializers_users import PasswordChangeSerializer, RegisterSerializer
from ..utils.email.sender import RegisterEmail, PasswordResetEmail
from ..utils.email.verifier import PasswordResetConfirm, RegisterConfirm


class RegisterAPIView(CreateAPIView, RegisterEmail):
    """
    View for registration.

    After entering user info new user will be created and
    user will receive an email with verification link which
    he should follow to finish registration. (Make his account active)
    """

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            return Response("Email already exists.",
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                            )

        user_id = serializer.data.get('id')
        user = get_object_or_404(UserProfile, id=user_id)
        self.email_register(request, user) # method from EmailRegister
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RegisterConfirmAPIView(APIView, RegisterConfirm):
    """
    View for confirm register.

    Simply activates user's account when user opens current view with his token.
    """

    def get(self, request, token):
        return self.register_confirm(token) # method from ConfirmRegister


class PasswordResetAPIView(APIView, PasswordResetEmail):
    """
    View for password reset.

    Takes 'email' from serializer and sends to it a mail with a link to proceed password reset.
    """

    def post(self, request):
        serializer = PasswordResetSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_object_or_404(UserProfile, email=email)
        self.email_password_reset(request, user) # method from EmailPasswordReset
        return Response({'message': 'Email send. Check your mailbox'}, status=status.HTTP_204_NO_CONTENT)


class PasswordResetConfirmAPIView(APIView, PasswordResetConfirm):
    """
    View for enter new password after reset. (Changes old one to new one)

    Takes 'new_password' from serializer and sets it as a new password for user.
    """

    def post(self, request, token):
        serializer = PasswordResetConfirmSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']
        return self.password_reset_confirm(new_password, token) # method from PasswordResetConfirm


class ChangePasswordAPIView(APIView):
    """
    UNDER DEVELOPMENT!
    """

    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
