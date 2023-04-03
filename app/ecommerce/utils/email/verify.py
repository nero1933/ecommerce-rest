from django.core.cache import cache

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app import settings
from ecommerce.models import UserProfile


class RegisterConfirm:

    def register_confirm(self, token):
        register_key = settings.USER_CONFIRMATION_KEY.format(token=token)
        user_info = cache.get(register_key) or {}

        if user_id := user_info.get('user_id'):
            user = get_object_or_404(UserProfile, id=user_id)
            user.is_active = True
            user.save(update_fields=['is_active'])
            cache.delete(register_key)
            return Response({'message': 'Successfully registered'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm:

    def password_reset_confirm(self, new_password, token):
        pswd_reset_key = settings.PASSWORD_CONFIRMATION_KEY.format(token=token)
        user_info = cache.get(pswd_reset_key) or {}

        if user_id := user_info.get('user_id'):
            user = get_object_or_404(UserProfile, id=user_id)
            user.set_password(new_password)
            user.save()
            cache.delete(pswd_reset_key)
            return Response({'message': 'Password updated successfully.'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
