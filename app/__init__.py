from flask import Flask
from flask_restful import Api
from .resources.product import Product, ProductList, ProductClearAll
from .db import db


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    api.add_resource(Product, "/product/<int:product_id>", "/product")
    api.add_resource(ProductList, "/products")
    api.add_resource(ProductClearAll, "/clear-products")

    # create db tables
    with app.app_context():
        print("Creating tables...")
        print(db.metadata.tables)  # Verifica que las tablas estén registradas
        db.create_all()

    return app
