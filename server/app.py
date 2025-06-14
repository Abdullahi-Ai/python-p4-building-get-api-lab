#!/usr/bin/env python3
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Bakery API"})

@app.route('/bakeries')
def get_bakeries():
    bakeries = [b.to_dict() for b in Bakery.query.all()]
    return make_response(jsonify(bakeries), 200)

@app.route('/bakeries/<int:id>')
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    return make_response(jsonify(bakery.to_dict()), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    goods = [b.to_dict() for b in baked_goods]
    return make_response(jsonify(goods), 200)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if baked_good:
        return make_response(jsonify(baked_good.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "No baked goods found"}), 404)