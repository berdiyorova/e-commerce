# Generated by Django 5.0.6 on 2024-07-07 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_orders_options_orders_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='total_price',
        ),
    ]
