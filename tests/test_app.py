import unittest
import random

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

        Category.get_or_create(name="test_Drink")

        # Create duplicated product
        Product.get_or_create(name="Duplicate", price=100, category_id=1)

        self.product_to_delete = Product.create(name="test_Product_Delete", price=10, category_id=1)

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
        self.assertEqual(len(response.json), 2)

    def test_products_post(self):
        unique_product_name = f"test_{random.randint(1, 1000000)}"
        response = self.app.post("/products", json={"name": unique_product_name, "price": "100", "category_id": 1})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], unique_product_name)
        self.assertEqual(float(response.json["price"]), 100)
        self.assertEqual(int(response.json["category"]["id"]), 1)

    def test_product_post_duplicate_name(self):
        response = self.app.post("/products", json={"name": "Duplicate", "price": 100, "category_id": 1})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Product with this name already exists")
        print(self.assertEqual(response.json["error"], "Product with this name already exists"))

    def test_product_post_invalid_data(self):
        response = self.app.post("/products", json={"name": "Invalid", "price": "invalid", "category_id": "Invalid"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Price must be a number")

    def test_product_delete_existing(self):
        response = self.app.delete(f"/products/{self.product_to_delete.id}")
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Product.get_or_none(Product.id == self.product_to_delete.id))
        print(response)

    def test_product_delete_non_existing(self):
        response = self.app.delete("/products/100000")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["error"], "Product not found")
        print(response)
