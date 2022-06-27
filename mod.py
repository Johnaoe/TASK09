from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from __init__ import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('User name', db.String(200), unique=True, nullable=False)
    email = db.Column('E.Mail', db.String(200), unique=True, nullable=False)
    pasw = db.Column('Password', db.String(200), unique=True, nullable=False)
    is_admin = db.Column('Administratorius', db.Boolean(), default=False)
    is_staf = db.Column('Darbuotojas', db.Boolean(), default=False)

    def __repr__(self) -> str:
        return self.name

class Cars(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column('Brand', db.String(30), nullable=False)
    model = db.Column('Model', db.String(30), nullable=False)
    years = db.Column('Production years', db.Integer, nullable=False)
    engin = db.Column('Car Engine', db.String(30), nullable=False)
    number = db.Column('Number Plate', db.String(15), nullable=False)
    vin_nr = db.Column('VIN code', db.String(17), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("user", lazy=True)

    def __repr__(self) -> str:
        return f'{self.number} - {self.brand} {self.model}'


class CarService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column('Service registration date', db.DateTime(), default = datetime.utcnow)
    status = db.Column('Service status', db.String(30), nullable=False)
    price = db.Column('Service price', db.Integer, nullable=False)
    issue = db.Column('Issue', db.String(300), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('Cars.id'))
    car = db.relationship("Cars", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", lazy=True)

    def __repr__(self) -> str:
        return f'{self.car} -- {self.status}'

class Admin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


