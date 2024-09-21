from flask import Flask
from flask_restful import Api
from .resources.product import Product, ProductList, ProductClearAll
from .db import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    api.add_resource(Product, "/product/<int:id>", "/product")
    api.add_resource(ProductList, "/products")
    api.add_resource(ProductClearAll, "/clear-products")

    return app
