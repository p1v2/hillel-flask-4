import unittest
from app import app, products


class ProductDeletionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        products.append({"id": 8, "name": "Marshmellow"})

    def test_delete_existing_product(self):
        response = self.app.delete(f'/products/7/')
        self.assertEqual(response.status_code, 204)

    def test_delete_non_existing_product(self):
        response = self.app.delete('/products/94/')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()


