from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    is_staff = serializers.HiddenField(default=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_staff')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
