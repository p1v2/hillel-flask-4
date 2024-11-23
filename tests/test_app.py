import unittest
import random
from http.client import responses

from peewee import SqliteDatabase

from app import app
from peewee_db import Product, Category

test_db = SqliteDatabase(":memory:")


# Use test DB
class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Make test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True

        # Use test DB
        test_db.bind([Product, Category])
        test_db.connect()
        test_db.create_tables([Product, Category])

        default_category = Category.create(name="Default")

        # Create duplicated product
        Product.create(name="Duplicate", price=100, category=default_category)
        self.product_delete = Product.create(name="Product_for_Deleting", price=150, category=default_category)
        self.deleteme = Product.create(name="DeleteMe", price=50, category=default_category)

    def tearDown(self):
        # Delete duplicated product
        Product.delete().where(Product.name == "Duplicate").execute()
        # Delete test products
        Product.delete().where(Product.name.startswith("test_")).execute()

        # Close test DB
        test_db.drop_tables([Product, Category])
        test_db.close()

    def test_products_get(self):
        response = self.app.get("/products")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)

    def test_products_post(self):
        unique_product_name = f"test_{random.randint(1, 1000000)}"
        response = self.app.post("/products", json={"name": unique_product_name, "price": "100"})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], unique_product_name)
        self.assertEqual(float(response.json["price"]), 100)

    def test_product_post_duplicate_name(self):
        response = self.app.post("/products", json={"name": "Duplicate", "price": 100})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Product with this name already exists")

    def test_product_post_invalid_data(self):
        response = self.app.post("/products", json={"name": "Invalid", "price": "invalid"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Price must be a number")

    # Test for deleting an existing product
    def test_product_delete(self):
        response = self.app.delete(f"/products/{self.product_delete.id}")
        self.app.delete(f"/products/{self.product_delete.id}")

        self.assertEqual(response.status_code, 204)

        # Verify if the product is deleted

        get_response = self.app.get(f"/products/{self.product_delete.id}")
        self.assertEqual(get_response.status_code, 404)

    # Test for deleting a non-existing product

    def test_product_delete_non_existing(self):
        # First, delete the product
        self.app.delete(f"/products/{self.deleteme.id}")

        # Then attempt to delete this product again
        response = self.app.delete(f"/products/{self.deleteme.id}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Product not found")
