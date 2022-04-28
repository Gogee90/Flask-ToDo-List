from functools import wraps
from flask import jsonify


def error_message(func):
    @wraps(func)
    def wrapper():
        try:
            return func()
        except Exception as e:
            return (
                jsonify({"error": type(e).__name__, "error_description": str(e)}),
                500,
            )

    return wrapper
