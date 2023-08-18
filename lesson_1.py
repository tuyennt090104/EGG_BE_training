from enum import Enum


class TypeProduct(Enum):
    Food = 0
    Drink = 1


class Product:
    name: str
    price: int
    type_product: TypeProduct
    date_time: str

    def __init__(self, name, price, type_product, data_time):
        self.name = name
        self.price = price
        self.type_product = type_product
        self.date_time = data_time

    def __str__(self):
        return f"{self.name} {self.price} {self.type_product} {self.date_time}"

    def __eq__(self, other):
        if isinstance(other, Product):
            return (self.name == other.name
                    and self.price == other.price
                    and self.type_product == other.type_product
                    and self.date_time == other.date_time)
        return False


class Container:
    products = []

    def add(self, product):
        self.products.append(product)

    def pop(self, product):
        print(product in self.products)
        if product in self.products:
            self.products.remove(product)

    def count(self):
        return len(self.products)

    def find(self, name):
        for product in [x for x in self.products if x.name == name]:
            print(product)

    def print(self):
        for product in self.products:
            print(product)


container = Container()
container.add(Product("a", 1, TypeProduct.Food, "2023-8-18"))
container.add(Product("a", 2, TypeProduct.Food, "2023-8-18"))
container.add(Product("a", 1, TypeProduct.Food, "2023-8-17"))
container.add(Product("b", 3, TypeProduct.Food, "2023-8-14"))
container.add(Product("c", 5, TypeProduct.Food, "2023-8-15"))
container.add(Product("c", 5, TypeProduct.Food, "2023-8-15"))
container.pop(Product("c", 5, TypeProduct.Food, "2023-8-15"))
container.print()
