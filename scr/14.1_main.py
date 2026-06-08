

class Product:
    " "
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    "Класс по подсчету категорий, товаров по категориям"
    name: str
    description: str
    products: list[Product]

    # Атрибуты класса (общие для всех объектов)
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счётчик категорий
        Category.category_count += 1

        # Увеличиваем счётчик товаров на количество товаров в категории
        Category.product_count += len(products)







    # Создание конструктора/инициализатора
    def __init__(self, name, surname, pay):      # Конструктор
        """Метод для инициализации экземпляра класса. Задаем значения атрибутам экземпляра."""
        self.name = name                         # Атрибуты (свойства) класса
        self.surname = surname
        self.pay = pay
        self.email = f'{self.name}.{self.surname}@proton.me'
        self.number_of_employees = 1             # Будет создан атрибут объекта

        Employee.number_of_employees += 1

    # Создаем методы для повышения зарплаты сотрудника
    def apply_raise(self):                       # Метод
        """Метод для повышения зарплаты сотрудника"""
        self.pay = self.pay * self.raise_amount

    def fullname(self):
        """Метод, который возвращает полное имя сотрудника"""
        return f'{self.surname} {self.name}'











if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category("Смартфоны",
                         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
                         [product1, product2, product3])

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)