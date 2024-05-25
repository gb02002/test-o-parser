from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from parsing_app.celery_tasks import start_parsing
from parsing_app.models import Products
from parsing_app.serializers import ProductSerializer


# Create your views here.

class Parser_Init(APIView):
    """Start parsing or return list"""
    def post(self, request) -> Response:
        """Starts parsing task with specified number of products."""
        try:
            products_count = max(1, min(int(request.data.get("products_count", 10)), 50))
            start_parsing.delay(products_count)
            return Response(data={"message": "Parsing task started successfully."}, status=status.HTTP_200_OK)
        except ValueError:
            return Response(data={"error": "Invalid value for products_count."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request) -> Response:
        """Entrypoint, returns all product names"""
        try:
            products_list = Products.all_list
            serializer = ProductSerializer(products_list, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Get_By_ID(APIView):
    """GET /v1/products/{product_id}/"""

    def get_product_id(self, product_id: int) -> int | None:
        """Retrieves id from request"""
        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return None
        return product_id

    def get(self, request, product_id: int) -> Response:
        """Entrypoint, returns object's data"""
        product_id = self.get_product_id(product_id)
        if product_id is None:
            return Response(data={"No content"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Products.objects.get(pk=product_id)
        except Products.DoesNotExist:
            return Response(data={"No content"}, status=status.HTTP_204_NO_CONTENT)

        product_serializer = ProductSerializer(product)
        return Response(data={'output': product_serializer.data}, status=status.HTTP_200_OK)
