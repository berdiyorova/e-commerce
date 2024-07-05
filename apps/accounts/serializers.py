from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User, UserAddress


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone', 'email', 'password')

    def create(self, validated_data):
        extra_fields = {
            'name': validated_data.get('name'),
            'phone': validated_data.get('phone')
        }
        user = User.objects.create_user(
            email=validated_data.get("email"), password=validated_data.get("password"), **extra_fields
        )
        return user

    def to_representation(self, instance):
        data = super(UserCreateSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class LoginSerializer(TokenObtainPairSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if user:
            self.user = user
        else:
            raise ValidationError({
                'success': False,
                'message': 'Sorry, login or password you entered is incorrect. Please, check and try again.'
            })
        data = self.user.token()
        data['email'] = self.user.email

        return data


class LoginRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ChangeUserInformation(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'phone', 'email', 'date_of_birth')

    def update(self, user, validated_data):
        user.name = validated_data.get('name', user.name)
        user.phone = validated_data.get('phone', user.phone)
        user.email = validated_data.get('email', user.email)
        user.date_of_birth = validated_data.get('date_of_birth', user.date_of_birth)
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('password_confirm'):
            raise serializers.ValidationError('Passwords do not match')

        return attrs


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        exclude = ('user', )
    def create(self, validated_data, request):
        name = validated_data.get('name')
        phone = validated_data.get('phone_number')
        email = validated_data.get('email')
        district = validated_data.get('district')
        street = validated_data.get('street')
        home = validated_data.get('home_number')
        porch = validated_data.get('porch')
        floor = validated_data.get('floor')
        apartment = validated_data.get('apartment')
        intercom = validated_data.get('intercom')
        user_address = UserAddress.objects.create(
            user=request.user,
            name=name,
            phone_number=phone,
            email=email,
            district=district,
            street=street,
            home_number=home,
            porch=porch,
            floor=floor,
            apartment=apartment,
            intercom=intercom
        )
        return user_address
