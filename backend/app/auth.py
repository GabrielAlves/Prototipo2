from flask import request, jsonify, current_app

def require_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("my-api-key")

        if not api_key or api_key != current_app.config["API_KEY"]:
            return jsonify({"error" : "Unauthorized"}), 401

        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper