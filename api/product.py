from flask import request
from flask.views import MethodView

from cache import cache
from models import Product, Review


class ProductView(MethodView):
    @staticmethod
    @cache.cached(timeout=10, query_string=True)
    def get(product_id: int):
        page = request.args.get('page', '1')
        page_size = request.args.get('page_size', '1')
        if page.isdigit():
            page = int(page)
        if page_size.isdigit():
            page_size = int(page_size)
        product = Product.get(id=product_id)
        if product:
            return product.to_dict(page=page, page_size=page_size)
        return dict(success=False, message='Product not found')

    @staticmethod
    def put(product_id: int):
        if request.json.get('title') is None:
            return dict(success=False, message='"title" is not defined')
        if request.json.get('text') is None:
            return dict(success=False, message='"text" is not defined')
        product = Product.get(id=product_id)
        if product:
            Review.create(product=product, **request.json)
            return dict(success=True)
        return dict(success=False, message='Product not found')
