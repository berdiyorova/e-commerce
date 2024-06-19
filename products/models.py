from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Category(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    category_name = models.CharField(max_length=200)
    category_image = models.ImageField(upload_to='images/', null=True, blank=True,)

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='images/', blank=True, null=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Attribute(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='attributes')

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=30)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')

    def __str__(self):
        return f'{self.attribute} = {self.value}'


class Discount(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='discounts', blank=True, null=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'
