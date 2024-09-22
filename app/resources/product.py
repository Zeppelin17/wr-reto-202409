from flask_restful import Resource, reqparse
from app.models.product_model import ProductModel
from app.services.product_service import Website, WebProductData
from datetime import datetime
from typing import Tuple


class Product(Resource):
    """Product manager"""

    def get(self, product_id: int) -> Tuple[dict, int]:
        product = ProductModel.find_by_id(product_id)
        if product:
            return product.json(), 200

        return {"message": f"Product with id {product_id} not found"}, 404

    def post(self) -> Tuple[dict, int]:
        parser = reqparse.RequestParser()
        parser.add_argument("url", type=str, required=True)
        parser.add_argument("price_trigger", type=float, required=True)
        data = parser.parse_args()

        webpage = Website(data.get("url"))
        web_data = WebProductData(webpage)
        product_data = {
            "name": web_data.product_title,
            "price": min(web_data.get_float_price_list()),
            "trigger": data.get("price_trigger"),
            "url": data.get("url"),
            "created": datetime.now(),
        }

        new_product = ProductModel(**product_data)
        try:
            new_product.save_to_db()
        except Exception as e:
            return {
                "message": "An error occurred creating the product",
                "errors": web_data.errors,
                "exception": str(e),
            }, 500

        return {"message": f"Item {new_product.id} created"}, 201

    def delete(self, product_id: int) -> Tuple[dict, int]:
        product = ProductModel.find_by_id(product_id)
        if product:
            product.delete_from_db()
            return {"message": f"Product with id {product_id} deleted"}, 200
        return {"message": f"Product with id {product_id} not found"}, 404

    def put(self, product_id: int) -> Tuple[dict, int]:
        product = ProductModel.find_by_id(product_id)
        if product:
            parser = reqparse.RequestParser()
            parser.add_argument("price_trigger", type=float, required=True)
            data = parser.parse_args()
            product.price_trigger = data.get("price_trigger")
            product.save_to_db()
            return {"message": f"Product with id {product_id} updated"}, 200


class ProductList(Resource):
    def get(self) -> Tuple[dict, int]:
        return {
            "products": [product.json() for product in ProductModel.find_all()]
        }, 200


class ProductClearAll(Resource):
    def get(self) -> dict:
        ProductModel.delete_all_from_db()
        return {"message": "All products deleted"}
