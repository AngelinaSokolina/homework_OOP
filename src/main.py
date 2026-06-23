class Product:
    "Класс для представления товара"

    name: str  # Название товара
    description: str  # Описание товара
    price: float  # Цена товара
    quantity: int  # Количество товара в наличии

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        "Инициализация товара"
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        '''Метод для отображения информации об объекте класса
        для пользователей'''
        return f'{self.name}, {self.price:.1f} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other: "Product") -> float:
        """Двойная проверка перед сложением"""

        # Проверка на одинаковые классы
        if not isinstance(other, type(self)):
            raise TypeError(f"Нельзя складывать {type(self).__name__} с {type(other).__name__}")

        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: dict) -> Product:
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def price(self) -> float:
        """Геттер: возвращает цену"""
        return self.__price

    @price.setter
    def price(self, user_price: float) -> None:
        """Сеттер: проверяет цену, НО НЕ УСТАНАВЛИВАЕТ НОВУЮ, если она <= 0"""
        if user_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = user_price

# Класс наследник
class Smartphone(Product):

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: int, model: str, memory: int, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

# Класс наследник
class LawnGrass(Product):

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    "Класс по подсчету категорий, товаров по категориям"

    name: str  # Название категории
    description: str  # Описание категории
    products: list[Product]  # Список товаров в категории

    # Атрибуты класса (общие для всех объектов)
    category_count = 0  # Общее количество категорий
    product_count = 0  # Общее количество товаров по всем категориям

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        "Инициализация категории"
        self.name = name
        self.description = description
        self.__products = products

        # Увеличиваем счётчик категорий
        Category.category_count += 1

        # Увеличиваем счётчик товаров на количество товаров в категории
        Category.product_count += len(products)

    def __str__(self) -> str:
        '''Метод для отображения информации об объекте класса
        для пользователей'''
        # Общее количество товаров только по этой категории
        total_quantity = sum(product.quantity for product in self.__products)
        return f'{self.name}, количество продуктов: {total_quantity} шт.'

    def add_product(self, product: Product) -> None:
        "Метод для добавления товара в категорию"
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> list:
        """Геттер возвращает копию списка товаров"""
        return self.__products.copy()
