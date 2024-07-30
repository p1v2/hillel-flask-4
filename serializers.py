from models import Product
from peewee_db import Product as PeeweeProduct, Category


def serialize_product(product: Product | PeeweeProduct):
    return product.model_dump()


def serialize_products(products: list[Product | PeeweeProduct]):
    return [product.model_dump() for product in products]


def serialize_categories(categories: list[Category]):
    return [category.model_dump() for category in categories]