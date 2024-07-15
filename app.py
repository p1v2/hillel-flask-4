from urllib import request

from flask import Flask, request

app = Flask(__name__)


products = []

# Rest API for data from the list


@app.route("/products", methods=["GET", "POST"])
def get_products():
    if request.method == "POST":
        # Add product to the list
        product = request.json
        products.append(product)
        return product
    elif request.method == "GET":
        return products
    else:
        # Return 405 Method Not Allowed
        return "Method Not Allowed", 405


@app.route("/products/<int:index>", methods=["GET", "PUT", "DELETE"])
def get_product(index):
    if request.method == "GET":
        # Return product by index
        return products[index]
    elif request.method == "PUT":
        # Update product by index
        product = request.json
        products[index] = product
        return product
    elif request.method == "DELETE":
        # Delete product by index
        product = products.pop(index)
        if product:
            return "", 204
        else:
            return "Product not found", 404
    else:
        # Return 405 Method Not Allowed
        return "Method Not Allowed", 405


if __name__ == "__main__":
    app.run(port=5002, debug=False)
