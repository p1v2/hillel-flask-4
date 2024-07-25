import json
from sqlite3 import IntegrityError
from urllib import request

from flask import Flask, request
from pydantic import ValidationError

from db import read_products, create_product, read_product, product_partial_update, delete_product
from models import ProductPayload
from serializers import serialize_products, serialize_product

app = Flask(__name__)


products = []

# Rest API for data from the list


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ValueError):
            return str(obj)

        return super().default(obj)


@app.route("/products", methods=["GET", "POST"])
def products_api():
    if request.method == "GET":
        products = read_products()

        return serialize_products(products)
    elif request.method == "POST":
        product_data = request.json

        try:
            product_payload = ProductPayload(**product_data)
        except ValidationError as error:
            return json.dumps(error.errors(), cls=CustomJSONEncoder), 400

        try:
            product = create_product(product_payload)
        except IntegrityError as error:
            if "UNIQUE constraint failed: product.name" in str(error):
                return {"error": "Product with this name already exists"}, 400
        else:
            return serialize_product(product), 201


@app.route("/products/<int:id>", methods=["GET", "PATCH", "DELETE"])
def product_api(id: int):
    if request.method == "GET":
        product = read_product(id)

        if product is None:
            return {"error": "Product not found"}, 404
        else:
            return serialize_product(product)
    elif request.method == "PATCH":
        update_data = request.json

        product_partial_update(id, update_data)

        updated_product = read_product(id)

        return serialize_product(updated_product)

    elif request.method == "DELETE":
        deleted_count = delete_product(id)

        if deleted_count == 0:
            return {"error": "Product not found"}, 404
        else:
            return "", 204
