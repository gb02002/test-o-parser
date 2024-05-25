from typing import Union

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Manager, QuerySet


# Create your models here.
class ProductManager(models.Manager):
    def full_list(self) -> Union[QuerySet['Products'], None]:
        """Retrieve products"""
        try:
            full_list = self.all()
            return full_list
        except self.model.DoesNotExist:
            return None


class Products(models.Model):
    """Products model"""

    products_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    description = models.TextField(max_length=2500)
    image_url = models.URLField(blank=True)
    discount = models.CharField(max_length=50)

    class Meta:
        unique_together = (('name', 'price'),)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name, self.price

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    objects = Manager()
    all_list = ProductManager()
