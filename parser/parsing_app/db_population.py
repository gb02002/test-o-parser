from django.core.exceptions import ValidationError
from parsing_app.models import Products, LastProducts


def populate_db(product_data):
    try:
        discount_percentage = round((product_data["discount"] / product_data["price"]) * 100)

        Products.objects.create(
            name=product_data["name"],
            price=product_data["price"],
            description=product_data["description"],
            image_url= product_data["image_url"],
            discount=discount_percentage
        )

        LastProducts.objects.create(
            name=product_data["name"],
            image_url= product_data["image_url"],
        )

    except ValidationError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# def populate_db(product_data):
#     try:
#         # Создаем или получаем продукт с указанным именем и ценой
#         product, created = Products.objects.get_or_create(
#             name=product_data["name"],
#             price=product_data["price"],
#             defaults={
#                 'description': product_data["description"],
#                 'image_url': product_data.get("image_url", ""),
#                 'discount': product_data["discount"]
#             }
#         )
#
#         # Если продукт был создан, то выведем сообщение об успешном создании
#         if created:
#             print(f"Product '{product.name}' created successfully.")
#         else:
#             product.description = product_data["description"]
#             product.image_url = product_data.get("image_url", "")
#             product.discount = product_data["discount"]
#             product.save()
#             print(f"Product '{product.name}' updated successfully.")
#     except ValidationError as e:
#         print(f"Validation error: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
