from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ecommerce.models.models_addresses import UserAddress
from ecommerce.serializers.serializers_addresses import UserAddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        queryset = UserAddress.objects.filter(user=self.request.user) \
            .select_related('address')

        return queryset


# class CountryViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Country.objects.all().order_by('id')
#     serializer_class = CountrySerializer
