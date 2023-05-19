from rest_framework import serializers

from ..models import Address, UserAddress


class AddressSerializer(serializers.ModelSerializer):
    # country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all())
    # country_id = serializers.PrimaryKeyRelatedField(read_only=True)
    # country_id = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    class Meta:
        model = Address
        fields = ['id',
                  'name',
                  'surname',
                  'street',
                  'unit_number',
                  'country',
                  'region',
                  'city',
                  'post_code',
                  'phone',
                  ]


class UserAddressSerializer(serializers.ModelSerializer):
    # https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault
    # Advanced field defaults
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    address = AddressSerializer()

    class Meta:
        model = UserAddress
        fields = ['id', 'address', 'user', 'is_default']

    def create(self, validated_data):
        # https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations
        # Writable nested representations
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        return UserAddress.objects.create(address=address, **validated_data)

    def update(self, instance, validated_data):
        # https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations
        # Writable nested representations
        address_data = validated_data.pop('address')
        address = instance.address

        instance.user = validated_data.get('user', instance.user)
        instance.is_default = validated_data.get('is_default', instance.is_default)
        instance.save()

        address.name = address_data.get('name', address.name)
        address.surname = address_data.get('surname', address.surname)
        address.street = address_data.get('street', address.street)
        address.unit_number = address_data.get('unit_number', address.unit_number)
        address.region = address_data.get('region', address.region)
        address.post_code = address_data.get('post_code', address.post_code)
        address.phone = address_data.get('phone', address.phone)
        address.country = address_data.get('country', address.country)
        address.save()

        return instance


# class CountrySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Country
#         fields = '__all__'