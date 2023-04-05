import uuid

import rest_framework.request
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework.reverse import reverse

from app import settings
from ecommerce.models import UserProfile


class SendLinkEmail:

    def _send_link(self,
                  request: rest_framework.request.Request,
                  user: UserProfile,
                  secret_key: str,
                  timeout: int,
                  reverse_name: str,
                  template: str,
                  subject: str,
                  ):
        """
        Method sends an email which contains a html template with a confirmation link for user.

        It generates a token, joins it with a secret key and sets the resul as a key in redis.
        The value is a dict with a key 'user_id' and a value of user's id. Then it generates
        a link with a path taken from 'reverse_name' and the 'token'. After that it loads
        a template and renders it with a context, pastes it as a string in email message.
        When all done it sends an email to the user.

        :param request: The HTTP request object.
        :param user: UserProfile's instance.
        :param secret_key: The secret key (located in settings).
                           Used to join with token and set as key in redis.
        :param timeout: The timeout variable (located in settings).
                        The maximum time to wait for a response from the email.
        :param reverse_name: For this reverse name will be generated link
                             which will be sent in the email.
        :param template: The path to the template which will be rendered in email.
        :param subject: The subject of the email.
        """
        token = uuid.uuid4().hex
        register_key = secret_key.format(token=token)
        cache.set(register_key, {'user_id': user.pk}, timeout=timeout)

        confirm_link = request.build_absolute_uri(
            reverse(reverse_name, kwargs={'token': token})
        )

        # https://docs.djangoproject.com/en/4.1/topics/email/
        # Sending alternative content types

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


class RegisterEmail(SendLinkEmail):

    def email_register(self,
                       request: rest_framework.request.Request,
                       user: UserProfile,
                       ):
        """
        Method sends an email with link to user for confirmation his email.

        It uses '_send_link' method with preset parameters for sending registration confirm emails.

        :param request: The HTTP request object.
        :param user: UserProfile's instance.
        """
        self._send_link(
            request,
            user,
            settings.USER_CONFIRMATION_KEY,
            settings.USER_CONFIRMATION_TIMEOUT,
            'register_confirm',
            'ecommerce/email_register.html',
            'Confirmation of Registration',
        )


class PasswordResetEmail(SendLinkEmail):

    def email_password_reset(self,
                             request: rest_framework.request.Request,
                             user: UserProfile,
                             ):
        """
        Method sends an email with link to user for entering new password (serializer).

        It uses '_send_link' method with preset parameters for password reset.

        :param request: The HTTP request object.
        :param user: UserProfile's instance.
        """
        self._send_link(
            request,
            user,
            settings.PASSWORD_CONFIRMATION_KEY,
            settings.PASSWORD_CONFIRMATION_TIMEOUT,
            'password_reset_confirm',
            'ecommerce/email_password_reset.html',
            'Password reset',
        )





    # def email_new_order(self):
    #     pass
    #
    # def email_shipped_order(self):
    #     pass
