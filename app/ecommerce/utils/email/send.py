import uuid

from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse

from app import settings
from ...models import UserProfile


class EmailSendLink:

    def _send_link(self,
                  request,
                  user,
                  secret_key,
                  timeout,
                  reverse_name,
                  template,
                  subject
                  ):
        """
        :param request:
        :param secret_key:
        :param timeout:
        :param reverse_name:
        :param template:
        :param subject:
        :return:
        """

        token = uuid.uuid4().hex  # generates token
        register_key = secret_key.format(token=token)  # add token to secret key
        # set 'register_key' as key and dict with user id as value in redis
        cache.set(register_key, {"user_id": user.id}, timeout=timeout)

        confirm_link = request.build_absolute_uri(
            reverse(reverse_name, kwargs={'token': token})
        )

        context = {
            'confirm_link': confirm_link,
        }

        html_body = render_to_string(template, context)

        message = EmailMultiAlternatives(
            subject=subject,
            body=f'{subject}\n{confirm_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        message.attach_alternative(html_body, "text/html")
        message.send(fail_silently=False)


class EmailRegister(EmailSendLink):

    def email_register(self, request, user):
        self._send_link(
            request,
            user,
            settings.USER_CONFIRMATION_KEY,
            settings.USER_CONFIRMATION_TIMEOUT,
            'register_confirm',
            'ecommerce/email_register.html',
            'Confirmation of Registration'
        )

class EmailPasswordReset(EmailSendLink):

    def email_password_reset(self, request, user):
        self._send_link(
            request,
            user,
            settings.PASSWORD_CONFIRMATION_KEY,
            settings.PASSWORD_CONFIRMATION_TIMEOUT,
            'password_reset_confirm',
            'ecommerce/email_password_reset.html',
            'Password reset'
        )




    # def reset_password(self):
    #     pass
    #
    # def send_new_order(self):
    #     pass
    #
    # def send_shipped_order(self):
    #     pass
