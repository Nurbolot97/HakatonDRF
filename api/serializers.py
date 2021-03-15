from rest_framework import serializers

from main.models import Category, Engine, Wheel, Display, User, Order



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





       

