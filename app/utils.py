from flask import jsonify, request

ALLOWED_UPDATE_FIELDS = {"name", "description", "price", "total_quantity", "available_quantity"}

def json_error(message, status=400):
    return jsonify({"error": message}), status

def extract_json():
    data = request.get_json(silent=True)
    if not data:
        return None
    return data

def sanitize_update_payload(payload: dict) -> dict:
    sanitized = {}
    for key, value in payload.items():
        if key in ALLOWED_UPDATE_FIELDS:
            sanitized[key] = value
    return sanitized
