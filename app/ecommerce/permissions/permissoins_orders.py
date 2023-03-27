from django.db import connection
from rest_framework.permissions import BasePermission


class NotEmptyShoppingCart(BasePermission):
    message = "Can't create an empty order"

    def has_permission(self, request, view):
        queryset = view.get_queryset()
        if request.method == 'OPTIONS':
            return True

        return bool(len(queryset))