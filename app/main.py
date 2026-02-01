from flask import Flask, jsonify
from app.routes import register_routes

app = Flask(__name__)
register_routes(app)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    import traceback
    traceback.print_exc()
    
    response = {"error": "Internal server error"}
    if app.debug:
        response["message"] = str(e)
        response["traceback"] = traceback.format_exc()
        
    return jsonify(response), 500

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google Cloud
    # Run, a webserver process such as Gunicorn will serve the app.
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
