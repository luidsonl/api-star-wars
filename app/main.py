import functions_framework
from flask import Flask, jsonify
from app.routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

@functions_framework.http
def api_star_wars(request):
    """
    HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`.
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>
    """
    # Cloud Functions (functions-framework) handles the request context.
    # We can use the app to dispatch the request.
    with app.test_request_context(
        path=request.path,
        base_url=request.base_url,
        query_string=request.query_string,
        method=request.method,
        headers=dict(request.headers),
        data=request.get_data(),
    ):
        try:
            rv = app.full_dispatch_request()
        except Exception as e:
            rv = app.handle_exception(e)
        return app.make_response(rv)
