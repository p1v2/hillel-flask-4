from datetime import datetime

from flask import Flask, request
from peewee import IntegrityError

from peewee_db import Product, Category
from serializers import serialize_products, serialize_categories

app = Flask(__name__)

products = [
    {"id": 1, "name": "Coca-Cola"},
    {"id": 2, "name": "Pepsi"},
    {"id": 3, "name": "Sprite"},
    {"id": 4, "name": "Banana Juice"},
    {"id": 5, "name": "Banana Smoothie"}
]
# Rest API for data from the list
import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


@app.route("/products", methods=["GET", "POST"])
def products_api():
    if request.method == "GET":
        start = datetime.now()
        products = Product.select(Product, Category).join(Category)

        resp = serialize_products(products)
        end = datetime.now()

@app.route("/products/", methods=["GET", "POST"])
def get_products():
    if request.method == "POST":
        product = request.json
        products.append(product)
        return product
    elif request.method == "GET":
        search_name = request.args.get('name', '').lower()
        if search_name:
            filtered_products = [product for product in products if search_name in product['name'].lower()]
        else:
            filtered_products = products
        return filtered_products
    else:
        # Return 405 Method Not Allowed
        return "Method Not Allowed", 405
        print(f"Time taken: {(end - start).total_seconds()} seconds")
        return resp
    elif request.method == "POST":
        product_data = request.json

        try:
            product = Product(**product_data)
            product.validate()
            product.save()
        except ValueError as error:
            return {"error": str(error)}, 400
        except IntegrityError as error:
            if "UNIQUE constraint failed: product.name" in str(error):
                return {"error": "Product with this name already exists"}, 400
            else:
                raise
        else:
            return product.model_dump(), 201


@app.route("/products/<int:id>", methods=["GET", "PATCH", "PUT", "DELETE"])
def product_api(id):
    product = Product.get_or_none(id=id)

    if product is None:
        return {"error": "Product not found"}, 404

@app.route("/products/<index>/", methods=["GET", "PUT", "DELETE"])
def get_product(index):
    if request.method == "GET":
        return products[index]
    if request.method == "GET":
        return product.model_dump()
    elif request.method == "PATCH":
        product_update_data = request.json

        for key, value in product_update_data.items():
            setattr(product, key, value)

        product.save()
        return product.model_dump()
    elif request.method == "PUT":
        update_data = request.json

        try:
            product.name = update_data["name"]
            product.price = update_data["price"]
            product.is_18_plus = update_data["is_18_plus"]
        except KeyError as error:
            return {"error": f"attribute {str(error)} is not set"}, 400

        product.save()
        return product.model_dump()
    elif request.method == "DELETE":
        # DON'T EVER DO THIS IN PRODUCTION
        # THIS DELETES THE WHOLE TABLE!!!!!!!
        # product.delete()

        product.delete_instance()
        return "", 204
    else:
        return {"error": "Method not allowed"}, 405


@app.route("/categories", methods=["GET", "POST"])
def categories_api():
    if request.method == "GET":
        categories = Category.select()

        return serialize_categories(categories)
    elif request.method == "POST":
        category_data = request.json

        category = Category(**category_data)
        category.save()

if __name__ == "__main__":
    app.run(port=5002, debug=True)
        return category.model_dump(), 201
