import unittest
import random
from datetime import datetime

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

        # Create duplicated product
        Category.get_or_create(name="TestCategory", created_at=datetime.now())
        Product.get_or_create(name="Duplicate", price=100, is_18_plus=False, category_id=1)

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
        self.assertEqual(len(response.json), 1)

    def test_products_post(self):
        unique_product_name = f"test_{random.randint(1, 1000000)}"
        response = self.app.post("/products", json={"name": unique_product_name, "price": "100",
                                                    "is_18_plus": False, "category_id": 1})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], unique_product_name)
        self.assertEqual(float(response.json["price"]), 100)

    def test_product_post_duplicate_name(self):
        response = self.app.post("/products", json={"name": "Duplicate", "price": 100,
                                                    "is_18_plus": False, "category_id": 1})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Product with this name already exists")

    def test_product_post_invalid_data(self):
        response = self.app.post("/products", json={"name": "Invalid", "price": "invalid",
                                                    "is_18_plus": False, "category_id": 1})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Price must be a number")

    # def create_product(self):
    #     product = Product(name="test_product", price=10.0, is_18_plus=False)
    #     return product

    def test_delete_existing_product(self):
        product = Product.get(name="Duplicate")
        response = self.app.delete(f"/products/{product.id}")
        self.assertEqual(response.status_code, 204)

        # Verify that the product has been deleted
        # deleted_product = Product.get_or_none(Product.id == product.id)
        # self.assertIsNone(deleted_product)

    def test_delete_non_existent_product(self):
        response = self.app.delete(f"/products/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Product not found"})


if __name__ == '__main__':
    unittest.main()
