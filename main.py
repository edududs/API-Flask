from functools import wraps

from flask import jsonify, request
from flask_restful import Resource

from models import API, APP, DB, Product, User


def commit_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            DB.session.commit()
            return result
        except Exception as e:
            DB.session.rollback()  # Em caso de exceção, faz rollback
            raise e

    return wrapper


# Resource para produtos
class ProductResource(Resource):

    def get(self, _id=None):
        if _id:
            product = Product.query.get_or_404(id)
            return jsonify(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                }
            )
        else:
            products = Product.query.all()
            output = []
            for product in products:
                product_data = {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                }
                output.append(product_data)

            return jsonify({"products": output})

    @commit_dec
    def post(self):
        data = request.get_json()
        new_product = Product(
            name=data["name"],
            description=data["description"],
            user_id=data.get("user_id", None),
        )
        DB.session.add(new_product)
        return jsonify({"message": "Product created successfully"})

    @commit_dec
    def put(self, _id):
        product = Product.query.get_or_404(_id)
        data = request.get_json()
        product.name = data["name"]
        product.description = data["description"]
        return jsonify({"message": "Product updated successfully"})

    @commit_dec
    def delete(self, _id):
        product = Product.query.get_or_404(_id)
        DB.session.delete(product)
        return jsonify({"message": "Product deleted successfully"})


class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return jsonify({"id": user.id, "name": user.name, "email": user.email})
        else:
            users = User.query.all()
            output = []
            for user in users:
                user_data = {"id": user.id, "name": user.name, "email": user.email}
                output.append(user_data)
            return jsonify({"users": output})

    @commit_dec
    def post(self):
        data = request.get_json()
        new_user = User(
            name=data["name"], email=data["email"], password=data["password"]
        )
        DB.session.add(new_user)
        return {"message": "User created successfully"}, 201

    @commit_dec
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        user.name = data["name"]
        user.email = data["email"]
        user.password = data["password"]
        return {"message": "User updated successfully"}

    @commit_dec
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        DB.session.delete(user)
        return {"message": "User deleted successfully"}


class UserProductResource(Resource):
    @commit_dec
    def post(self, user_id, product_id):
        user = User.query.get_or_404(user_id)
        product = Product.query.get_or_404(product_id)
        user.products.append(product)
        return jsonify({"message": "Product assigned to user successfully"})

    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        products = user.products
        output = []
        for product in products:
            product_data = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
            }
            output.append(product_data)
        return jsonify({"user_products": output})


# Adicionando os recursos à API
API.add_resource(ProductResource, "/products", "/product/<int:id>")
API.add_resource(UserResource, "/users", "/user/<int:user_id>")
API.add_resource(
    UserProductResource,
    "/user/<int:user_id>/assign_product/<int:product_id>",
    "/user/<int:user_id>/products",
)

if __name__ == "__main__":
    APP.run(debug=True)
