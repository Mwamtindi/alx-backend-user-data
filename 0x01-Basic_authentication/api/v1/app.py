#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth variable to None
auth = None

# Load correct authe'n system based on the env variable AUTH_TYPE
AUTH_TYPE = os.getenv("AUTH_TYPE")
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


# Before request handler to filter every request
@app.before_request
def before_request():
    """Handle request filtering before processing"""
    if auth is None:
        return  # Do nothing if no auth instance

    # Excluded paths that don't require authentication
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    # Skip filtering for excluded paths
    if request.path in excluded_paths:
        return

    # Check if the path requires authentication
    if auth.require_auth(request.path, excluded_paths):
        # Check for authorization header
        if auth.authorization_header(request) is None:
            abort(401)  # Unauthorized

        # Check if there's a valid current user (for auth'd user)
        if auth.current_user(request) is None:
            abort(403)  # Forbidden


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.route('/api/v1/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app.route('/api/v1/unauthorized', strict_slashes=False)
def unauthorized() -> str:
    """GET /api/v1/unauthorized
    Raises a 401 error"""
    abort(401)


@app.route('/api/v1/forbidden', strict_slashes=False)
def forbidden() -> str:
    """GET /api/v1/forbidden
    Raises a 403 error"""
    abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
