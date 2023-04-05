from rest_framework import serializers

from ..models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'phone', 'password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    # def create(self, validated_data):
    #     user = UserProfile.objects.create_user(
    #         validated_data['email'],
    #         validated_data['name'],
    #         validated_data['phone'],
    #         validated_data['password']
    #     )
    #
    #     return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})

        return value