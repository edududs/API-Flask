from flask import Flask, jsonify
from flask_login import UserMixin
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
APP.config["SECRET_KEY"] = "super-secret"

DB = SQLAlchemy(APP)
API = Api(APP)


# Modelo de dados
class Product(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), nullable=False)
    description = DB.Column(DB.String(225), nullable=False)
    user_id = DB.Column(
        DB.Integer, DB.ForeignKey("user.id"), nullable=True, default=None
    )

    def __repr__(self):
        return f"Product(name={self.name}, description={self.description})"


class User(DB.Model, UserMixin):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), nullable=False)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    password = DB.Column(DB.String(80), nullable=False)
    products = DB.relationship("Product", backref="user", lazy=True)
    active = DB.Column(DB.Boolean())
    roles = DB.relationship(
        "Role", secondary="user_roles", backref=DB.backref("users", lazy="dynamic")
    )

    def __repr__(self):
        return f"User(name={self.name}, email={self.email})"


# Definindo os modelos de usuário e papel (role)
class Role(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), unique=True)
    description = DB.Column(DB.String(255))


# Definindo a associação entre usuários e papéis
class UserRoles(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"))
    role_id = DB.Column(DB.Integer, DB.ForeignKey("role.id"))


with APP.app_context():
    DB.create_all()
