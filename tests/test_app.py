import unittest
import random

from peewee import SqliteDatabase

from app import app
from peewee_db import Product

test_db = SqliteDatabase(":memory:")


# Use test DB
class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Make test client
        self.app = app.test_client()
        # Propagate exceptions to the test client
        self.app.testing = True

        # Use test DB
        test_db.bind([Product])
        test_db.connect()
        test_db.create_tables([Product])

        # Create duplicated product
        Product.get_or_create(name="Duplicate", price=100)

        # Create product to be deleted
        Product.get_or_create(name="Product_for_Deleting", price=150)

        # Product for test "deleting a non-existing product"
        self.deleteme = Product.get_or_create(name="DeleteMe", price=50)

    def tearDown(self):
        # Delete duplicated product
        Product.delete().where(Product.name == "Duplicate").execute()
        # Delete test products
        Product.delete().where(Product.name.startswith("test_")).execute()

        # Close test DB
        test_db.drop_tables([Product])
        test_db.close()

    def test_products_get(self):
        response = self.app.get("/products")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

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
        response = self.app.delete("/products", json={"name": "Product_for_Deleting", "price": 150})

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.json["message"], "Product deleted successfully")

        # Verify if the product is deleted
        get_response = self.app.get("/products", json={"name": "Product_for_Deleting", "price": 150})
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_response.json["error"], "Product not found")

    # Test for deleting a non-existing product

    def test_product_delete_non_existing(self):
        # First, delete the product
        self.app.delete(f"/products/{self.deleteme.id}")

        # Then attempt to delete this product again
        response = self.app.delete(f"/products/{self.deleteme.id}")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Product not found")
