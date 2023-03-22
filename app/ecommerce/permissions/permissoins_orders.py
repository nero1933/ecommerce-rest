from django.db import connection
from rest_framework.permissions import BasePermission


class NotEmptyShoppingCart(BasePermission):
    message = "Can't create an empty order"

    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True

        return bool(len(view.get_queryset()))