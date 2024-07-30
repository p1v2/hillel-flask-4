import requests


def test_product_create(name):
    # Create a new product
    url = "http://127.0.0.1:5002/products"

    data = {
        "name": name,
        "price": 80,
        "is_18_plus": False,
        "category_id": 1
    }

    response = requests.post(url, json=data)

    print(response.status_code)
    print(response.text)


def test_product_delete():
    # Delete a product by index
    url = "http://localhost:5002/products/10"

    response = requests.delete(url)

    print(response.status_code)
    print(response.text)


def test_product_update():
    # Update a product by index
    url = "http://localhost:5002/products/3"

    data = {
        "is_18_plus": False
    }

    response = requests.patch(url, json=data)

    print(response.status_code)
    print(response.text)


def test_category_create():
    # Create a new category
    url = "http://localhost:5002/categories"

    data = {
        "name": "Drinks"
    }

    response = requests.post(url, json=data)

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    # Generate 1000 products
    for i in range(100):
        test_product_create(f"Product {i}")
