from flask import Blueprint, request, jsonify, has_request_context

about_bp = Blueprint('about', __name__)

@about_bp.route('/', methods=['GET'])
def about():
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

