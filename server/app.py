#!/usr/bin/env python3
import os
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json_encoder = None  # This is to ensure SQLAlchemy models are properly serialized

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


# Index route for testing purposes
@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


# Restaurant resource
class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [restaurant.to_dict() for restaurant in restaurants]


class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return restaurant.to_dict(with_pizzas=True)
        else:
            return {"error": "Restaurant not found"}, 404

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        else:
            return {"error": "Restaurant not found"}, 404


# Pizza resource
class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [pizza.to_dict() for pizza in pizzas]


# RestaurantPizza resource
class RestaurantPizzaResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=int, required=True, help="Price is required")
        parser.add_argument('pizza_id', type=int, required=True, help="Pizza ID is required")
        parser.add_argument('restaurant_id', type=int, required=True, help="Restaurant ID is required")
        args = parser.parse_args()

        # Validate inputs
        if not (1 <= args['price'] <= 30):
            return {"errors": ["Validation error: price must be between 1 and 30"]}, 400

        pizza = Pizza.query.get(args['pizza_id'])
        restaurant = Restaurant.query.get(args['restaurant_id'])

        if not pizza or not restaurant:
            return {"errors": ["Validation error: Invalid pizza_id or restaurant_id"]}, 400

        restaurant_pizza = RestaurantPizza(price=args['price'], pizza=pizza, restaurant=restaurant)

        db.session.add(restaurant_pizza)
        db.session.commit()

        return restaurant_pizza.to_dict(), 201


# Add resources to API
api.add_resource(RestaurantListResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzaListResource, '/pizzas')
api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas')


if __name__ == "__main__":
    app.run(port=5555, debug=True)