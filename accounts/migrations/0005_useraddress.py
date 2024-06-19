# Generated by Django 5.0.4 on 2024-05-06 00:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_delete_useraddress_user_date_of_birth_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^\\*?1?\\d{9,13}$')])),
                ('street', models.CharField(max_length=100)),
                ('home_number', models.CharField(max_length=10)),
                ('porch', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('floor', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('apartment', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('intercom', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^(([0-9]{1,4}))$')])),
            ],
            options={
                'verbose_name': 'User address',
                'verbose_name_plural': 'User addresses',
            },
        ),
    ]
