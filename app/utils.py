from flask import jsonify, request

def json_error(message, status=400):
    return jsonify({"error": message}), status

def extract_json():
    data = request.get_json(silent=True)
    if not data:
        return None
    return data
