from rest_framework.permissions import BasePermission

from ..models import Order


class IsCreatorOrReadOnly(BasePermission):
    """
    Custom permission to allow only the creator of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the creator of the review.
        return obj.user == request.user


class IsReviewAllowed(BasePermission):
    message = 'You must be a customer who has purchased the product to comment.'

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            obj = Order.objects\
                .prefetch_related('order_item')\
                .filter(pk=view.kwargs['order_id'],
                        user=request.user,
                        order_status=4,
                        order_item__pk=view.kwargs['order_item_id'],
                        )

            return obj.exists()
