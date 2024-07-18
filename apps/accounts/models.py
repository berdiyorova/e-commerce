from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'admin'
        OWNER = 'OWNER', 'owner'
        EMPLOYEE = 'EMPLOYEE', 'employee'
        DELIVERY = 'DELIVERY', 'delivery'
        CLIENT = 'CLIENT', 'client'

    name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CLIENT)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, validators=[RegexValidator(r'^\*?1?\d{9,13}$')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    USERNAME_FIELD = "email"
    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh_token': str(refresh)
        }


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(r'^\*?1?\d{9,13}$')])
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    home_number = models.CharField(max_length=10)
    porch = models.IntegerField(validators=[MinValueValidator(1)])
    floor = models.IntegerField(validators=[MinValueValidator(0)])
    apartment = models.IntegerField(validators=[MinValueValidator(1)])
    intercom = models.CharField(max_length=10, validators=[RegexValidator(r'^(([0-9]{1,4}))$')])

    def __str__(self):
        return f'{self.district} district, {self.street} street, {self.home_number}/{self.apartment}'

    class Meta:
        verbose_name = 'User address'
        verbose_name_plural = 'User addresses'
