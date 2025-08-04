# server/app_test.py
import json
from server.app import app
from server.models import db, Bakery, BakedGood

class TestApp:
    def test_creates_baked_goods(self):
        with app.app_context():
            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if af:
                db.session.delete(af)
                db.session.commit()

            response = app.test_client().post(
                '/baked_goods',
                data={
                    "name": "Apple Fritter",
                    "price": 2.0,
                    "bakery_id": 1
                }
            )

            af = BakedGood.query.filter_by(name="Apple Fritter").first()

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            assert af.id

    def test_updates_bakeries(self):
        with app.app_context():
            mb = Bakery.query.filter_by(id=1).first()
            mb.name = "ABC Bakery"
            db.session.commit()

            response = app.test_client().patch(
                '/bakeries/1',
                data={"name": "Your Bakery"}
            )

            updated = Bakery.query.get(1)

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert updated.name == "Your Bakery"

    def test_deletes_baked_goods(self):
        with app.app_context():
            af = BakedGood.query.filter_by(name="Apple Fritter").first()
            if not af:
                af = BakedGood(name="Apple Fritter", price=2.0, bakery_id=1)
                db.session.add(af)
                db.session.commit()

            response = app.test_client().delete(f'/baked_goods/{af.id}')

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            assert not BakedGood.query.filter_by(name="Apple Fritter").first()
