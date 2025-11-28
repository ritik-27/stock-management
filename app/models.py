from mongoengine import Document, StringField, FloatField, IntField, BooleanField, signals
from config import Config

RESTOCK_THRESHOLD = Config.RESTOCK_THRESHOLD

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


def calculate_need_restock(total_quantity: int, available_quantity: int) -> bool:
    try:
        total_quantity = int(total_quantity)
        available_quantity = int(available_quantity)
    except (TypeError, ValueError):
        return True

    if total_quantity <= 0:
        return True
    return available_quantity < (total_quantity * RESTOCK_THRESHOLD)


def pre_save_product(sender, document, **kwargs):
    if document.available_quantity > document.total_quantity:
        document.available_quantity = document.total_quantity

    document.need_restock = calculate_need_restock(document.total_quantity, document.available_quantity)


signals.pre_save.connect(pre_save_product, sender=Product)
