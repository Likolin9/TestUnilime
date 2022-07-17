from flask import Blueprint

api_bp = Blueprint('api', __name__)

from api.product import ProductView

api_bp.add_url_rule('/products/<int:product_id>', view_func=ProductView.as_view('products'), methods=['GET', 'PUT'])
