from flask import Flask, jsonify
from flasgger import Swagger
from app.routes import register_routes

app = Flask(__name__)
app.url_map.strict_slashes = False

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
    'specs_route': '/apidocs/',
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"'
        }
    }
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
    
    # Use o código de status do erro HTTP se for um
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
    # Isto é usado apenas quando executado localmente. Ao implantar no Google Cloud
    # Run, um processo de servidor web como o Gunicorn servirá o app.
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
