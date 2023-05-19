data = {
    "email": 'test1@test.com',
    "payment_method": 1,
    "shipping_address": {
        'name': 'r',
        'surname': 'n',
        'street': 'dm 15',
        'country': 'Ukraine',
        'region': 'ch',
        'city': 'ch',
        'post_code': 49000,
        'phone': '+380956663321',
    },
    "shipping_method": 1,
}
from django.core.cache import cache

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from app import settings
from ecommerce.models import UserProfile


class RegisterConfirm:

    def register_confirm(self, token: str):
        """
        Method makes user active.

        It joins secret key with token. Result is a key for entry in redis.
        Tries to get a value which supposed to be a dict with "user_id" key
        and user's id value. Gets user by id and sets his "is_active" to True
        after what deletes entry in redis. HTTP 204 if everything done or
        HTTP 400 if entry has expired.

        :param token: Takes token that was generated while registration
        :return: HTTP 204 if everything done or HTTP 400 if entry has expired.
        """
        register_key = settings.USER_CONFIRMATION_KEY.format(token=token)
        user_info = cache.get(register_key) or {}

        if user_id := user_info.get('user_id'):
            user = get_object_or_404(UserProfile, pk=user_id)
            user.is_active = True
            user.save(update_fields=['is_active'])
            cache.delete(register_key)
            return Response({'message': 'Successfully registered'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirm:

    def password_reset_confirm(self, new_password, token):
        """
        Method changes user's password.

        It joins secret key with token. Result is a key for entry in redis.
        Tries to get a value which supposed to be a dict with "user_id" key
        and user's id value. Gets user by id and sets him new password after
        what deletes entry in redis. HTTP 204 if everything done or HTTP 400
        if entry has expired.

        :param new_password: New password which will be set for user.
        :param token: Token that was generated when send request to reset password
        :return: HTTP 204 if everything done or HTTP 400 if entry has expired.
        """
        pswd_reset_key = settings.PASSWORD_CONFIRMATION_KEY.format(token=token)
        user_info = cache.get(pswd_reset_key) or {}

        if user_id := user_info.get('user_id'):
            user = get_object_or_404(UserProfile, id=user_id)
            user.set_password(new_password)
            user.save()
            cache.delete(pswd_reset_key)
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
