import uuid

from django.core.cache import cache
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse

from app import settings
from ...models import UserProfile


class EmailSendLink:

    def send_link(self,
                  request,
                  user_id,
                  secret_key,
                  timeout,
                  template,
                  context,
                  subject
                  ):

        user = get_object_or_404(UserProfile, id=user_id)

        token = uuid.uuid4().hex  # generates token
        register_key = secret_key.format(token=token)  # add token to secret key
        # set 'register_key' as key and dict with user id as value in redis
        cache.set(register_key, {"user_id": user.id}, timeout=timeout)

        confirm_link = request.build_absolute_uri(
            reverse('test', kwargs={'token': token})
        )

        html_body = render_to_string(template, context)

        message = EmailMultiAlternatives(
            subject=subject,
            body=f'{subject}\n{confirm_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)

class EmailRegister:

    def email_register(self, request, user_id):
        user = get_object_or_404(UserProfile, id=user_id)

        token = uuid.uuid4().hex  # generates token
        register_key = settings.USER_CONFIRMATION_KEY.format(token=token)  # add token to secret key
        # set 'register_key' as key and dict with user id as value in redis
        cache.set(register_key, {"user_id": user.id}, timeout=settings.USER_CONFIRMATION_TIMEOUT)

        confirm_link = request.build_absolute_uri(
            reverse('test', kwargs={'token': token})
        )

        context = {
            'confirm_link': confirm_link,
        }

        html_body = render_to_string("ecommerce/email_register.html", context)

        message = EmailMultiAlternatives(
            subject='Registration confirm',
            body=f'Registration confirm\n{confirm_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)







    # def reset_password(self):
    #     pass
    #
    # def send_new_order(self):
    #     pass
    #
    # def send_shipped_order(self):
    #     pass
