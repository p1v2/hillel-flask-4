from urllib import request

from flask import Flask, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Coca-Cola"},
    {"id": 2, "name": "Pepsi"},
    {"id": 3, "name": "Sprite"},
    {"id": 4, "name": "Banana Juice"},
    {"id": 5, "name": "Banana Smoothie"}
]
# Rest API for data from the list


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


@app.route("/products/<index>/", methods=["GET", "PUT", "DELETE"])
def get_product(index):
    if request.method == "GET":
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
    app.run(port=5002, debug=True)
