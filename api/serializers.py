from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from main.models import Category, Engine, Wheel, Display, User, Order, Comment



class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'


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

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class CategorySerializer(serializers.ModelSerializer):

    name_category = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'name_category', 'slug', 'id'
        ]


class BaseProductSerializer:

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)


class EnginesSerializer(BaseProductSerializer, serializers.ModelSerializer):

    power = serializers.CharField(required=True)
    made_location = serializers.CharField(required=True)
    material = serializers.CharField(required=True)

    class Meta:
        model = Engine
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    text = serializers.CharField(required=True)
    engine = serializers.PrimaryKeyRelatedField(queryset=Engine.objects)

    class Meta:
        model = Comment
        fields = ['text', 'engine', 'id']


class DisplaysSerializer(BaseProductSerializer, serializers.ModelSerializer):

    diagonal = serializers.CharField(required=True)
    display = serializers.CharField(required=True)
    resolution = serializers.CharField(required=True)
    ram = serializers.CharField(required=True)

    class Meta:
        model = Display
        fields = '__all__'


class WheelsSerializer(BaseProductSerializer, serializers.ModelSerializer):

    size = serializers.CharField(required=True)
    made_location = serializers.CharField(required=True)
    material = serializers.CharField(required=True)

    class Meta:
        model = Wheel
        fields = '__all__'





       

