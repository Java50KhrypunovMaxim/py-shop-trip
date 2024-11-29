from math import sqrt

from app.car import Car
from app.shop import Shop


class Customer:
    def __init__(self, name: str, product_cart: dict, location: list[int],
                 money: float, car: Car) -> None:
        self.name = name
        self.product_cart = product_cart
        self.location = location
        self.money = money
        self.car = car

    def calculate_distance(self, shop_location: list[int]) -> float:
        x1, y1 = self.location
        x2, y2 = shop_location
        return round(sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)

    def calculate_trip_cost(self, shop_location: list[int],
                            fuel_price: float) -> float:
        distance = self.calculate_distance(shop_location)
        return round(2 * distance * (self.car.fuel_consumption / 100)
                     * fuel_price, 2)

    def calculate_product_cost(self, shop_products: dict) -> float:
        total_cost = 0
        for product, qty in self.product_cart.items():
            if product in shop_products:
                total_cost += shop_products[product] * qty
        return total_cost

    def calculate_total_cost(self, shop: Shop, fuel_price: float) -> float:
        trip_cost = self.calculate_trip_cost(shop.location, fuel_price)
        product_cost = self.calculate_product_cost(shop.products)
        return trip_cost + product_cost

    def update_location(self, new_location: list[int]) -> None:
        self.location = new_location
