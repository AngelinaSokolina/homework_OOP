from mypy.dmypy.client import status_parser
from mypyc.common import SELF_NAME


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
        self.price = price
        self.quantity = quantity



class Category:
    "Класс по подсчету категорий, товаров по категориям"

    name: str  # Название категории
    description: str  # Описание категории
    products: list[Product]  # Список товаров в категории

    # Атрибуты класса (общие для всех объектов)
    category_count = 0  # Общее количество категорий
    product_count = 0  # Общее количество товаров

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        "Инициализация категории"
        self.name = name
        self.description = description
        self.__products = products


        # Увеличиваем счётчик категорий
        Category.category_count += 1

        # Увеличиваем счётчик товаров на количество товаров в категории
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        "Метод для добавления товара в категорию"
        self.__products.append(product)
        Category.product_count += 1

    @property
    def product_list(self) -> str:
        "Геттер, который возвращает строку со списком товаров"
        result_str = ""
        for product in self.__products:
            result_str += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
        return result_str


