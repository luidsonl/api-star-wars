from flask import Blueprint, request, jsonify, has_request_context

about_bp = Blueprint('about', __name__)

@about_bp.route('/', methods=['GET'])
def about():
    """
    About the Star Wars API
    ---
    tags:
      - About
    responses:
      200:
        description: API information
        schema:
          properties:
            name:
              type: string
            author:
              type: string
            github:
              type: string
            docs:
              type: string
            demo_client:
              type: string
    """
    if has_request_context():
        base_url = request.url_root.rstrip('/')
    else:
        base_url = ""
    return jsonify({
        'name': 'API Star Wars',
        'author': 'Luidson Lima Santos',
        'github': 'https://github.com/luidsonl/api-star-wars',
        'docs': base_url + '/apidocs/',
        'demo_client': 'https://api-star-wars-frontend.vercel.app/'
    })
