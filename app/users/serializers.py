from rest_framework import serializers
from .models import CustomUser

# class RegisterSerializer(serializers.Serializer):
#     password = serializers.Serializer
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password')