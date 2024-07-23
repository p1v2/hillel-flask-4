from models import Product


def serialize_product(product: Product):
    return product.dict()


def serialize_products(products: list[Product]):
    return [product.dict() for product in products]
