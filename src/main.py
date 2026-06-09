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
        self.products = products

        # Увеличиваем счётчик категорий
        Category.category_count += 1

        # Увеличиваем счётчик товаров на количество товаров в категории
        Category.product_count += len(products)
