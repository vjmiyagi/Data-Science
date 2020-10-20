from os import getenv
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()


APP = Flask(__name__)


DB = SQLAlchemy(APP)


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(150), index=True, nullable=False)
    email = DB.Column(DB.String(150), index=True, unique=True, nullable=False)
    password = DB.Column(DB.String(30), unique=True, nullable=False)
    password_hash = DB.Column(DB.String(120), nullable=False)
    over_21 = DB.Column(DB.Boolean, index=True, nullable=False)
    med_or_rec = DB.Column(DB.String(40), index=True, nullable=True)
    med_stat = DB.Column(DB.String(360), index=True, nullable=True)
    user_effect = DB.Column(DB.String(150), index=True, nullable=False)

    def set_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.email


class Strain(DB.Model):
    strain_id = DB.Column(DB.Integer, primary_key=True)
    strain = DB.Column(DB.String(30), unique=True, nullable=False)
    species_id = DB.Column(DB.Integer, DB.ForeignKey("species.species_id"))
    species = DB.relationship("Species", backref=DB.backref("species", lazy=True))
    rate = DB.Column(DB.Float, nullable=True)

    def __repr__(self):
        return "<Strain %r>" % self.strain


class Species(DB.Model):
    species_id = DB.Column(DB.Integer, primary_key=True)
    species = DB.Column(DB.String(6), nullable=False)

    def __repr__(self):
        return "<Species %r>" % self.species


class Effects(DB.Model):
    effects_id = DB.Column(DB.Integer, primary_key=True)
    effects = DB.Column(DB.String(9), nullable=False)

    def __repr__(self):
        return "<Effect %r>" % self.effects


class StrainEffects(DB.Model):
    se_id = DB.Column(DB.Integer, primary_key=True)
    strain_id = DB.Column(DB.Integer, DB.ForeignKey("strain.strain_id"))
    strain =  DB.relationship("Strain", backref=DB.backref("strain"), lazy=True)
    effect_id = DB.Column(DB.Integer, DB.ForeignKey("effects.effects_id"))
    effect = DB.relationship("Effects", backref=DB.backref("effects", lazy=True))

    def __repr__(self):
        return "<StrainEffects %r>"  % self.effect


class Flavor(DB.Model):
    flavor_id = DB.Column(DB.Integer, primary_key=True)
    flavor = DB.Column(DB.String(9), nullable=False)

    def __repr__(self):
        return "<Flavor %r" % self.flavor

class StrainFlavor(DB.Model):
    sf_id = DB.Column(DB.Integer, primary_key=True)
    strain_id = DB.Column(DB.Integer, DB.ForeignKey("strain.strain_id"))
    strain =  DB.relationship("Strain", backref=DB.backref("strain"), lazy=True)
    flavor_id = DB.Column(DB.Integer, DB.ForeignKey("flavor.flavor_id"))
    flavor = DB.relationship("Flavor", backref=DB.backref("flavor", lazy=True))

    def __repr__(self):
        return "<Flavor %r>" % self.flavor


class Shops(DB.Model):
    shop_id = DB.Column(DB.Integer, primary_key=True)
    shop = DB.Column(DB.String(65), unique=True, nullable=False)
    log = DB.Column(DB.Float, nullable=True)
    lng = DB.Column(DB.Float, nullable=True)
    address = DB.Column(DB.String(65), nullable=True)
    city = DB.Column(DB.String(30), nullable=False)
    state = DB.Column(DB.String(2), nullable=False)
    zip = DB.Column(DB.Integer, nullable=True)

    def __repr__(self):
        return "<Shops %r>" % self.shop
#
#
# class Med_Symptoms(DB.Model):
#     symptoms_id = DB.Column(DB.Integer, primary_key=True)
#     user_med_stat = DB.Column(DB.String(360), index=True, nullable=True)
#     relief = DB.Column(DB.String(150), index=True, nullable=True)
#     user_med = DB.Column(DB.Integer, DB.ForeignKey("user.user_id"))
#     user_stat = DB.relationship("User", backref=DB.backref("relief", lazy=True))
#
#     def __repr__(self):
#         return "<Med_Symptoms %r>" % self.user_med_stat
