from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


# Modelo de dados
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(225), nullable=False)

    def __repr__(self):
        return f"Product(name={self.name}, description={self.description})"

with app.app_context():
    db.create_all()


# Rotas da API
@app.route("/products", methods=["GET"])
def get_products():
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


@app.route("/product/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(
        {"id": product.id, "name": product.name, "description": product.description}
    )


@app.route("/product", methods=["POST"])
def create_product():
    data = request.get_json()
    new_product = Product(name=data["name"], description=data["description"])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"})


@app.route("/product/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data["name"]
    product.description = data["description"]
    db.session.commit()
    return jsonify({"message": "Product updated successfully"})


@app.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
