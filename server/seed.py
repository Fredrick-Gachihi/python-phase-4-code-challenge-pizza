

from app import app, db
from models import Restaurant, Pizza, RestaurantPizza

def seed_data():
    with app.app_context():
        # Delete existing data to avoid duplicates
        print("Deleting existing data...")
        db.session.query(RestaurantPizza).delete()
        db.session.query(Restaurant).delete()
        db.session.query(Pizza).delete()
        db.session.commit()

        # Create Restaurants
        print("Creating restaurants...")
        shack = Restaurant(name="Karen's Pizza Shack", address='address1')
        bistro = Restaurant(name="Sanjay's Pizza", address='address2')
        palace = Restaurant(name="Kiki's Pizza", address='address3')

        # Create Pizzas
        print("Creating pizzas...")
        cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
        pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
        california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")

        # Create RestaurantPizzas
        print("Creating RestaurantPizzas...")
        pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=1)
        pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=4)
        pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=5)

        # Add objects to session and commit
        db.session.add_all([shack, bistro, palace, cheese, pepperoni, california, pr1, pr2, pr3])
        db.session.commit()

        print("Seeding done!")

if __name__ == '__main__':
    seed_data()

