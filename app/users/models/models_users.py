from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from phonenumber_field.modelfields import PhoneNumberField

from ecommerce.models.models_shopping_cart import ShoppingCart
from .models_addresses import Address


class UserProfileManager(BaseUserManager):
    """ Helps Django work with our custom user model. """

    def create_user(self, email, name, phone, password=None):
        """ Creates a new user profile object. """

        if not email:
            raise ValueError('Users must have an email address.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone)

        user.set_password(password)
        user.save(using=self.db)

        # Creates a shopping cart for the user
        ShoppingCart.objects.create(user=user)

        return user

    def create_superuser(self, email, name, phone, password):
        """ Creates and saves a new superuser with given details. """

        user = self.create_user(email, name, phone, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self.db)

        # Creates a shopping cart for the user
        ShoppingCart.objects.create(user=user)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represents a 'user profile' inside our system. """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone = PhoneNumberField()
    address = models.ManyToManyField(Address, through='UserAddress', related_name='address_to_user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def get_full_name(self):
        """ Used to get a users full name. """

        return self.name

    def get_short_name(self):
        """ Used to get a users short name. """

        return self.name

    def __str__(self):
        """ Convert an object to string. """

        return self.email
