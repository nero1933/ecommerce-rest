import re

from django.core import mail
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ecommerce.models import UserProfile


def get_link_from_message(message):
    message = mail.outbox[0].body
    regex = r"(?P<url>https?://[^\s]+)"
    match = re.search(regex, message)
    link = match.group("url")
    return link


class RegisterEmailTestCase(APITestCase):

    def test_register_user(self):
        """
        Try to register user and follow the confirmation link.
        """

        data = {
            "email": "test@test.com",
            "name": "test",
            "phone": '+380956665544',
            "password": '12345678',
            "password_confirmation": '12345678',
        }

        # Try to register
        response = self.client.post(reverse('register'), data, format='json')
        user_id = response.data.get('id')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the email was sent
        self.assertEqual(len(mail.outbox), 1, 'email with a verification link must be send')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'Code must be 201')

        # Check 'is_active' status of created user before opening link from email
        self.assertEqual(user.is_active, False, 'Before opening link from email "is_active" status of the user must be True')

        # Get confirmation link from message
        message = mail.outbox[0].body
        link = get_link_from_message(message)

        # Follow the confirmation link
        response = self.client.get(link, format='json')
        user = get_object_or_404(UserProfile, pk=user_id)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        # Check 'is_active' status of created user after opening link from email
        self.assertEqual(user.is_active, True, 'After opening link from email "is_active" status of the user must be True')


class PasswordResetEmailTestCase(APITestCase):

    def setUp(self):
        user = UserProfile.objects \
            .create_user(email='test@test.com',
                         name='test',
                         phone='+380951112233',
                         password='12345678'
                         )

        user.is_active = True
        user.save()

        self.user = user

    def test_password_reset(self):
        """
        Try to reset password, follow the confirmation link and enter nwe password.
        """

        data = {'email': 'test@test.com', 'password': '12345678'}

        # Try to log in
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')

        data = {'email': self.user.email}

        # Try to reset password
        response = self.client.post(reverse('password_reset'), data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        # Get confirmation link from message
        message = mail.outbox[0].body
        link = get_link_from_message(message)

        data = {'new_password': '87654321', 'new_password_confirmation': '87654321'}

        # Follow the confirmation link
        response = self.client.post(link, data, format='json')

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'Code must be 204')

        data = {'email': 'test@test.com', 'password': '87654321'}

        # Try to log in with new credentials
        response = self.client.post(reverse('token_obtain_pair'), data)

        # Check that the response has a success status code
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Code must be 200')
