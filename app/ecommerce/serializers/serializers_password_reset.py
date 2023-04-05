from rest_framework import serializers

# from .serializers_revews import ReviewSerializer
# from ..models.models_products import Product, ProductItem, ProductItemSizeQuantity, Image


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    new_password_confirmation = serializers.CharField(style={"input_type": "password"},write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirmation = attrs.pop('new_password_confirmation', None)
        if len(new_password) < 8:
            raise serializers.ValidationError("Passwords must be at lest 8 characters.")

        if new_password != new_password_confirmation:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs