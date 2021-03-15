from user_accounts.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, label='Password',
        required=True, style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, label='Confirm password',
        required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'password', 'password2', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'The 2 passwords are differ'})
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'The email must be unique'})
        return attrs



