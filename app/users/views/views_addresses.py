from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from ..models.models_addresses import UserAddress
from ..models.models_users import Address
from ..serializers.serializers_addresses import AddressSerializer, UserAddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = UserAddressSerializer

    # def get_queryset(self):
    #     user_id = self.request.user.pk
    #     queryset = Address.objects.filter(address_to_user__pk=user_id) \
    #         .prefetch_related('address_to_user') \
    #         .select_related('country') \
    #
    #     return queryset

    def get_queryset(self):
        user_id = self.request.user.pk
        queryset = UserAddress.objects.filter(user=user_id) \
            .select_related('address') \
            .select_related('address__country') \

        return queryset