# app/routes/product_routes.py
from flask import jsonify, request
from mongoengine.errors import ValidationError, DoesNotExist
from app.models import Product
from app.utils import json_error, extract_json, sanitize_update_payload

def register_routes(app):
    # Create product
    @app.route("/product", methods=["POST"])
    def create_product():
        data = extract_json()
        if data is None:
            return json_error("Request body must be valid JSON", 400)

        required = ["name", "price", "total_quantity", "available_quantity"]
        missing = [f for f in required if f not in data]
        if missing:
            return json_error(f"Missing required fields: {', '.join(missing)}", 400)

        try:
            product = Product(
                name=str(data["name"]),
                description=str(data.get("description", "")),
                price=float(data["price"]),
                total_quantity=int(data["total_quantity"]),
                available_quantity=int(data["available_quantity"]),
            )
            product.save()
            return jsonify(product.to_dict()), 201
        except (ValueError, TypeError):
            return json_error("Invalid data types for one or more fields", 400)
        except ValidationError as e:
            return json_error(str(e), 400)

    # Get all products
    @app.route("/product", methods=["GET"])
    def get_products():
        products = Product.objects()
        return jsonify([p.to_dict() for p in products]), 200

    # Get product by id
    @app.route("/product/<string:product_id>", methods=["GET"])
    def get_product(product_id):
        try:
            p = Product.objects.get(id=product_id)
        except (DoesNotExist, ValidationError):
            return json_error("Product not found", 404)
        return jsonify(p.to_dict()), 200

    # Update product
    @app.route("/product/<string:product_id>", methods=["PUT"])
    def update_product(product_id):
        data = extract_json()
        if data is None:
            return json_error("Request body must be valid JSON", 400)

        try:
            p = Product.objects.get(id=product_id)
        except (DoesNotExist, ValidationError):
            return json_error("Product not found", 404)

        updates = sanitize_update_payload(data)
        print(updates)
        if not updates:
            return json_error("No valid updatable fields provided", 400)

        try:
            if "name" in updates:
                p.name = str(updates["name"])
            if "description" in updates:
                p.description = str(updates["description"])
            if "price" in updates:
                p.price = float(updates["price"])
            if "total_quantity" in updates:
                p.total_quantity = int(updates["total_quantity"])
            if "available_quantity" in updates:
                p.available_quantity = int(updates["available_quantity"])
            if "available_quantity" in updates and "total_quantity" in updates:
                av = int(updates["available_quantity"])
                tot = int(updates["total_quantity"])

                if av > tot:
                    return json_error("available_quantity cannot be greater than total_quantity", 400)

            print("Before save:", p.to_dict())
            p.save()
        except (ValueError, TypeError):
            return json_error("Invalid data types for one or more fields", 400)
        except ValidationError as e:
            return json_error(str(e), 400)

        return jsonify(p.to_dict()), 200

    # Delete product
    @app.route("/product/<string:product_id>", methods=["DELETE"])
    def delete_product(product_id):
        try:
            p = Product.objects.get(id=product_id)
            p.delete()
            return jsonify({"message": "Product deleted"}), 200
        except (DoesNotExist, ValidationError):
            return json_error("Product not found", 404)

    # Check restock status for a specific product
    @app.route("/restock/<string:product_id>", methods=["GET"])
    def check_restock(product_id):
        try:
            p = Product.objects.get(id=product_id)
        except (DoesNotExist, ValidationError):
            return json_error("Product not found", 404)

        return jsonify({
            "id": str(p.id),
            "need_restock": bool(p.need_restock),
            "available_quantity": int(p.available_quantity),
            "total_quantity": int(p.total_quantity)
        }), 200

    # Manually update restock flag for a product
    @app.route("/restock/update/<string:product_id>", methods=["PUT"])
    def update_restock_status(product_id):
        data = extract_json()
        if data is None:
            return json_error("Request body must be valid JSON", 400)

        if "need_restock" not in data:
            return json_error("Missing required field: need_restock", 400)

        val = data["need_restock"]
        if isinstance(val, bool):
            flag = val
        elif isinstance(val, (int, float)):
            flag = bool(val)
        elif isinstance(val, str):
            v = val.strip().lower()
            if v in ("true", "1", "yes", "y"):
                flag = True
            elif v in ("false", "0", "no", "n"):
                flag = False
            else:
                return json_error("Field 'need_restock' must be boolean", 400)
        else:
            return json_error("Field 'need_restock' must be boolean", 400)

        try:
            p = Product.objects.get(id=product_id)
        except (DoesNotExist, ValidationError):
            return json_error("Product not found", 404)

        try:
            p.update(set__need_restock=flag)
            p.reload()
        except ValidationError as e:
            return json_error(str(e), 400)

        return jsonify(p.to_dict()), 200

    # List all products that need restock
    @app.route("/restock/list", methods=["GET"])
    def list_restock_items():
        products = Product.objects(need_restock=True)
        return jsonify([p.to_dict() for p in products]), 200
