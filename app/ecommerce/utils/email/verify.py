from django.core.cache import cache

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app import settings
from ecommerce.models import UserProfile


class ConfirmRegister:

    def confirm_register(self, token):
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
