from mongoengine import Document, StringField, FloatField, IntField, BooleanField
from config import Config

class Product(Document):
    meta = {"collection": "products"}
    name = StringField(required=True, max_length=255)
    description = StringField()
    price = FloatField(required=True, min_value=0)
    total_quantity = IntField(required=True, min_value=0)
    available_quantity = IntField(required=True, min_value=0)
    need_restock = BooleanField(default=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "total_quantity": int(self.total_quantity),
            "available_quantity": int(self.available_quantity),
            "need_restock": bool(self.need_restock),
        }
