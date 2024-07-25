import os
from datetime import datetime

from peewee import SqliteDatabase, Model, TextField, FloatField, BooleanField, DateTimeField, ForeignKeyField

db_path = os.path.join(os.path.dirname(__file__), 'data.db')
db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    name = TextField(unique=True, null=False)
    created_at = DateTimeField(default=datetime.now)

    def validate(self):
        if not self.name:
            raise ValueError("Name can't be empty")

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at
        }


class Product(BaseModel):
    name = TextField(unique=True, null=False)
    price = FloatField(null=False)
    is_18_plus = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    category = ForeignKeyField(Category, backref='products')

    def validate(self):
        if not self.name:
            raise ValueError("Name can't be empty")

        if not self.price:
            raise ValueError("Price can't be empty")

        try:
            float(self.price)
        except ValueError:
            raise ValueError("Price must be a number")

        if float(self.price) < 0:
            raise ValueError("Price can't be negative")

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "is_18_plus": self.is_18_plus,
            "created_at": self.created_at,
            "category": self.category and self.category.model_dump(),
        }


if __name__ == '__main__':
    db.connect()
    db.create_tables([Category, Product])
    db.close()
