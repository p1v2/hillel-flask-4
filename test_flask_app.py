import requests


def test_product_create():
    # Create a new product
    url = "http://localhost:5002/products"

    data = {
        "id": 2,
        "name": "Pepsi"
    }

    response = requests.post(url, json=data)

    print(response.status_code)
    print(response.text)


def test_product_delete():
    # Delete a product by index
    url = "http://localhost:5002/products/8"

    response = requests.delete(url)

    print(response.status_code)
    print(response.text)


def test_product_update():
    # Update a product by index
    url = "http://localhost:5002/products/2"

    data = {
        "name": "7up"
    }

    response = requests.put(url, json=data)

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    test_product_delete()
