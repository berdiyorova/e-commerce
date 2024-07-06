from django.db import models
from django.core.validators import MinValueValidator

from accounts.models import User, UserAddress
from products.models import Products, AttributeValue


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    subtotal = models.FloatField()
    attributes = models.ManyToManyField(AttributeValue, related_name='attributes')

    def __str__(self):
        return f'{self.user} | {self.product}'


class Orders(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ("-created_at",)

    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        IN_PROGRESS = 'in_progress', 'In_progress'
        DELIVERED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'
        FINISHED = 'finished', 'Finished'

    class PaymentType(models.TextChoices):
        BY_CARD = 'by_card', 'By_card'
        CASH = 'cash', 'Cash'
        APPLE_PAY = 'apple_pay', 'Apple_pay'

    class PaymentStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(CartItem, related_name='orders')
    total_price = models.FloatField()
    status = models.CharField(max_length=20, choices=Status.choices)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self): return self.created_at
