import uuid

from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.mail import send_mail
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
from ..utils.users import get_tokens_for_user


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def get_object(self):
        obj = UserProfile.objects.get(pk=self.request.user.id)
        return obj

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     print(serializer.data)
    #
    #     user = UserProfile.objects.get(pk=serializer.data['id'])
    #
    #     if not user.is_active:
    #         token = uuid.uuid4().hex
    #         redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
    #         cache.set(redis_key, {"user_id": user.id}, timeout=settings.USER_CONFIRMATION_TIMEOUT)
    #
    #         confirm_link = self.request.build_absolute_uri(
    #             reverse('register_confirm', kwargs={'token': token})
    #         )
    #
    #         message = _(f'Follow this link {confirm_link}\n'
    #                     f'to confirm!\n')
    #
    #         send_mail(
    #             subject=_('Please confirm your registration!'),
    #             message=message,
    #             from_email='neroigo.1933@gmail.com',
    #             recipient_list=[user.email, ]
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
def register_confirm(request):
    message = f'test'

    send_mail(
        subject=_('TEST'),
        message=message,
        from_email='neroigo.1933@gmail.com',
        recipient_list=['nero1933@protonmail.com', ]
        )

    print(request)
    return Response(status=status.HTTP_201_CREATED)

    # redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
    # user_info = cache.get(redis_key) or {}
    #
    # if user_id := user_info.get('user_id'):
    #     user = get_object_or_404(UserProfile, id=user_id)
    #     user.is_active = True
    #     user.save()
    #     return Response(status=status.HTTP_200_OK)
    # else:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)

        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):

    def post(self, request):
        logout(request)
        return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)