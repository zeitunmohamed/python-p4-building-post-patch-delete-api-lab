# server/app.py
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from server.models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def get_bakeries():
    bakeries = [b.to_dict() for b in Bakery.query.all()]
    return make_response(bakeries, 200)

@app.route('/bakeries/<int:id>')
def get_bakery(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if not bakery:
        return make_response({"error": "Bakery not found"}, 404)
    return make_response(bakery.to_dict(), 200)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response([bg.to_dict() for bg in baked_goods], 200)

@app.route('/baked_goods/most_expensive')
def most_expensive():
    bg = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(bg.to_dict(), 200)

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_bg = BakedGood(
        name=data.get('name'),
        price=float(data.get('price')),
        bakery_id=int(data.get('bakery_id'))
    )
    db.session.add(new_bg)
    db.session.commit()
    return jsonify(new_bg.to_dict()), 201

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return {"error": "Bakery not found"}, 404

    data = request.form
    if "name" in data:
        bakery.name = data["name"]

    db.session.commit()
    return jsonify(bakery.to_dict()), 200

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    bg = BakedGood.query.get(id)
    if not bg:
        return {"error": "Not found"}, 404

    db.session.delete(bg)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
