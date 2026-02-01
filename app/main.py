from flask import Flask, jsonify
from flasgger import Swagger
from app.routes import register_routes

app = Flask(__name__)

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'Star Wars API',
    'uiversion': 3,
    'description': 'API for managing Star Wars characters and favorites',
    'contact': {
        'name': 'API Support',
        'url': 'http://www.example.com/support',
        'email': 'support@example.com',
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
    },
    'version': '1.0.0',
    'specs_route': '/apidocs/'
}

swagger = Swagger(app)
register_routes(app)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    from werkzeug.exceptions import HTTPException
    
    traceback.print_exc()
    
    # Use the status code of the HTTP error if it is one
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    
    response = {
        "error": "Internal server error" if code == 500 else getattr(e, 'name', 'Error'),
        "status_code": code
    }
    
    if app.debug:
        response["message"] = str(e)
        response["traceback"] = traceback.format_exc()
        
    return jsonify(response), code

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google Cloud
    # Run, a webserver process such as Gunicorn will serve the app.
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
