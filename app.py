from datetime import datetime

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
        products[id] = product
        return product
    elif request.method == "DELETE":
        product = (p for p in products if p["id"] == id), None

        if id not in product:
            return "Product Not Found", 404
        else:
            products[:] = [p for p in products if p["id"] != id]
            return '', 204
    else:
        # Return 405 Method Not Allowed
        return "Method Not Allowed", 405
        

if __name__ == "__main__":
    app.run(port=5002, debug=True)
