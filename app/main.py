import json
from datetime import datetime

from app.car import Car
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:

    with open("config.json", "r") as file:
        config = json.load(file)

    fuel_price = config["FUEL_PRICE"]

    shops = [
        Shop(shop["name"], shop["location"], shop["products"])
        for shop in config["shops"]
    ]

    customers = [
        Customer(
            customer["name"],
            customer["product_cart"],
            customer["location"],
            customer["money"],
            Car(customer["car"]["brand"], customer["car"]["fuel_consumption"])
        )
        for customer in config["customers"]
    ]

    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")
        shop_costs = {}

        for shop in shops:
            total_cost = customer.calculate_total_cost(shop, fuel_price)
            print(f"{customer.name}'s trip to {shop.name} "
                  f"costs {total_cost: .2f}")
            shop_costs[shop.name] = total_cost

        best_shop_name = min(shop_costs, key=shop_costs.get)
        min_cost = shop_costs[best_shop_name]

        if min_cost > customer.money:
            print(f"{customer.name} doesn't have enough money "
                  f"to make a purchase in any shop\n")
            continue

        best_shop = next(shop for shop in shops if shop.name == best_shop_name)
        print(f"{customer.name} rides to {best_shop.name}\n")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Date: {current_time}")
        print(f"Thanks, {customer.name}, "
              f"for your purchase!\nYou have bought: ")

        product_cost = customer.calculate_product_cost(best_shop.products)
        for product, qty in customer.product_cart.items():
            if product in best_shop.products:
                cost = qty * best_shop.products[product]
                print(f"{qty} {product} for {cost: .2f} dollars")

        print(f"Total cost is {product_cost: .2f}\nSee you again!\n")

        customer.update_location(best_shop.location)
        customer.money -= min_cost

        print(f"{customer.name} rides home.")
        customer.update_location(config["customers"][0]["location"])
        print(f"{customer.name} now has {customer.money: .2f} dollars\n")


shop_trip()
