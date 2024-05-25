from rest_framework import serializers
from parsing_app.models import Products
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.WARNING)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description',  'image_url', 'discount']
