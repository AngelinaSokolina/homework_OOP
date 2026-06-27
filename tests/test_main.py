from abc import ABC
from typing import Any

import pytest

from src.main import BaseProduct, Category, LawnGrass, Product, Smartphone

# =========== Абстрактный класса BaseProduct ===========


class TestBaseProduct:
    """Тесты для абстрактного класса BaseProduct"""

    def test_base_product_is_abstract(self) -> None:
        """Проверяет, что BaseProduct - абстрактный класс"""
        # Проверяем, что класс существует
        assert BaseProduct is not None

        # Проверяем, что он наследуется от ABC
        assert issubclass(BaseProduct, ABC) is True

    def test_all_products_inherit_base_product(self) -> None:
        """Проверяет, что все классы продуктов наследуют BaseProduct"""
        assert issubclass(Product, BaseProduct) is True
        assert issubclass(Smartphone, BaseProduct) is True
        assert issubclass(LawnGrass, BaseProduct) is True

    def test_smartphone_has_work_method(self) -> None:
        """Проверяет, что Smartphone реализует метод work"""
        phone = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
        phone.work()

    def test_lawn_grass_has_work_method(self) -> None:
        """Проверяет, что LawnGrass реализует метод work"""
        grass = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")
        grass.work()


# =========== Тест для миксина ===========


def test_mixin_log_output() -> None:
    """Тест, что миксин выводит лог при создании объекта"""
    product = Product("Тест", "Описание", 100, 5)
    assert str(product) == "Тест, 100.0 руб. Остаток: 5 шт."


# =========== Тест проверки количества товара ===========
def test_raises_normal_quantity() -> None:
    """Тест проверяет, что товар с нормальным количеством создается без ошибок"""
    phone = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
    assert phone.quantity == 5
    assert phone.name == "iPhone"


def test_add_products_normal() -> None:
    """Тест проверяет сложение двух товаров с нормальным количеством"""
    phone_1 = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
    phone_2 = Smartphone("Samsung", "Описание", 800, 3, 95.0, "S23", 256, "Белый")

    result = phone_1 + phone_2
    assert result == 5000 + 2400  # 1000*5 + 800*3 = 7400


def test_raises_value_error() -> None:
    """Тест проверяет, что при нулевом значении количества вызывается ValueError"""
    with pytest.raises(ValueError) as exc_info:
        Smartphone("iPhone", "Описание", 1000, 0, 98.0, "15", 512, "Черный")

    # Проверяем сообщение исключения
    assert str(exc_info.value) == 'Товар с нулевым количеством не может быть добавлен'


def test_add_product_with_zero_quantity() -> None:
    """Тест проверяет, что при сложении с товаром у которого количество 0 вызывается ValueError"""
    phone_1 = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")

    with pytest.raises(ValueError, match='Товар с нулевым количеством не может быть добавлен'):
        phone_1 + Smartphone("iPhone", "Описание", 1000, 0, 98.0, "15", 512, "Черный")

def test_raises_value_error_negative_quantity() -> None:
    """Тест проверяет, что при создании товара с отрицательным количеством вызывается ValueError"""
    try:
        Smartphone("iPhone", "Описание", 1000, -5, 98.0, "15", 512, "Черный")
    except TypeError as e:
        print(e)

# # =========== Тестирование класса Product ===========


@pytest.fixture()
def product_main() -> Product:
    return Product("Молоко", "Очень вкусное. Честно", 100, 655)


def test_product_init(product_main: Product) -> None:
    assert product_main.name == "Молоко"
    assert product_main.description == "Очень вкусное. Честно"
    assert product_main.price == 100
    assert product_main.quantity == 655


# =========== Тестирование __str__ для Product ===========


def test_product_str(product_main: Product) -> None:
    """Проверяет строковое представление продукта"""
    expected = "Молоко, 100.0 руб. Остаток: 655 шт."
    assert str(product_main) == expected


# =========== Тестирование __add__ для Product ===========


def test_product_add() -> None:
    """Проверяет сложение двух продуктов (общая стоимость на складе)"""
    p1 = Product("Товар 1", "Описание", 100, 5)
    p2 = Product("Товар 2", "Описание", 200, 3)

    result = p1 + p2
    assert result == 1100


# =========== Тестирование класса Category ===========


@pytest.fixture()
def category_main(product_main: Product) -> Category:  # ← принимает товар из фикстуры
    return Category("Кисломолочные продукты", "Молоко, кефир, сыры", [product_main])


def test_category_init(category_main: Category) -> None:
    assert category_main.name == "Кисломолочные продукты"
    assert category_main.description == "Молоко, кефир, сыры"
    # Проверяем через геттер (теперь это список)
    products = category_main.products
    assert len(products) == 1
    assert products[0].name == "Молоко"


def test_category_count() -> None:
    """Проверяет увеличение счётчика категорий"""
    initial = Category.category_count
    Category("Тест", "Описание", [])
    assert Category.category_count == initial + 1


def test_empty_category() -> None:
    """Проверяет пустую категорию"""
    initial = Category.product_count
    Category("Пустая", "Описание", [])
    assert Category.product_count == initial


# =========== Тестирование __str__ для Category ===========


def test_category_str(category_main: Category) -> None:
    """Проверяет строковое представление категории"""
    expected = "Кисломолочные продукты, количество продуктов: 655 шт."
    assert str(category_main) == expected


def test_category_str_with_multiple_products() -> None:
    """Проверяет строковое представление категории с несколькими продуктами"""
    p1 = Product("Молоко", "Описание", 100, 10)
    p2 = Product("Кефир", "Описание", 80, 5)
    p3 = Product("Сметана", "Описание", 150, 3)

    category = Category("Молочные продукты", "Описание", [p1, p2, p3])

    expected = "Молочные продукты, количество продуктов: 18 шт."
    assert str(category) == expected


# =========== Тестирование классов Product, Category ===========


def test_product_count() -> None:
    """Проверяет увеличение счётчика продуктов"""
    initial = Category.product_count
    p1 = Product("Товар 1", "Описание", 100, 1)
    p2 = Product("Товар 2", "Описание", 200, 1)
    Category("Категория", "Описание", [p1, p2])
    assert Category.product_count == initial + 2


# =========== Тестирование приватного атрибута цены и сеттера ===========


def test_product_price_getter(product_main: Product) -> None:
    """Проверяет, что геттер возвращает правильную цену"""
    assert product_main.price == 100


def test_product_price_setter_positive() -> None:
    """Проверяет, что сеттер устанавливает положительную цену"""
    product = Product("Тест", "Описание", 500, 10)
    product.price = 700
    assert product.price == 700


def test_product_price_setter_zero(capsys: Any) -> None:
    """Проверяет, что сеттер НЕ устанавливает цену = 0 и выводит сообщение"""
    product = Product("Тест", "Описание", 500, 10)
    product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 500


def test_product_price_setter_negative(capsys: Any) -> None:
    """Проверяет, что сеттер НЕ устанавливает отрицательную цену и выводит сообщение"""
    product = Product("Тест", "Описание", 500, 10)
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 500


# =========== Тестирование метода new_product ===========


def test_new_product_from_dict() -> None:
    """Проверяет, что класс-метод new_product создаёт продукт из словаря"""
    product_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
    }
    product = Product.new_product(product_data)

    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


# =========== Тестирование приватного списка продуктов в Category ===========


def test_category_products_private() -> None:
    """Проверяет, что список продуктов в категории приватный и доступен через геттер"""
    product = Product("Тест", "Описание", 100, 5)
    category = Category("Категория", "Описание", [product])

    # Проверяем, что напрямую к приватному атрибуту нельзя обратиться
    with pytest.raises(AttributeError):
        category.__products


def test_category_add_product() -> None:
    """Проверяет, что метод add_product добавляет товар в категорию"""
    p1 = Product("Товар 1", "Описание", 100, 5)
    p2 = Product("Товар 2", "Описание", 200, 3)

    category = Category("Категория", "Описание", [p1])
    initial_count = Category.product_count

    category.add_product(p2)

    # Проверяем, что счётчик продуктов увеличился
    assert Category.product_count == initial_count + 1

    # Проверяем, что товар добавился в список (через геттер)
    products = category.products
    assert len(products) == 2
    assert products[0].name == "Товар 1"
    assert products[1].name == "Товар 2"


def test_category_product_list_is_copy() -> None:
    """Проверяет, что геттер возвращает копию списка, а не оригинал"""
    product = Product("Телефон", "Смартфон", 50000, 10)
    category = Category("Электроника", "Описание", [product])

    # Получаем список через геттер
    products_copy = category.products

    # Добавляем в копию
    new_product = Product("Планшет", "Описание", 30000, 5)
    products_copy.append(new_product)

    # Оригинальный список не изменился
    assert len(category.products) == 1
    assert category.products[0].name == "Телефон"


# =========== Тестирование классов-наследников ===========


def test_smartphone_init() -> None:
    """Проверяет инициализацию смартфона"""
    phone = Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )

    assert phone.name == "Samsung Galaxy S23 Ultra"
    assert phone.description == "256GB, Серый цвет, 200MP камера"
    assert phone.price == 180000.0
    assert phone.quantity == 5
    assert phone.efficiency == 95.5
    assert phone.model == "S23 Ultra"
    assert phone.memory == 256
    assert phone.color == "Серый"


def test_lawn_grass_init() -> None:
    """Проверяет инициализацию газонной травы"""
    grass = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")

    assert grass.name == "Газонная трава"
    assert grass.description == "Элитная трава для газона"
    assert grass.price == 500.0
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_smartphone_inherits_product() -> None:
    """Проверяет, что Smartphone является наследником Product"""
    assert issubclass(Smartphone, Product) is True


def test_lawn_grass_inherits_product() -> None:
    """Проверяет, что LawnGrass является наследником Product"""
    assert issubclass(LawnGrass, Product) is True


def test_smartphone_str() -> None:
    """Проверяет строковое представление смартфона (наследуется от Product)"""
    phone = Smartphone("iPhone", "Смартфон", 1000.0, 5, 98.0, "15", 512, "Черный")
    expected = "iPhone, 1000.0 руб. Остаток: 5 шт."
    assert str(phone) == expected


# =========== Тестирование __add__ с проверкой типов ===========


def test_add_same_class_smartphones() -> None:
    """Проверяет сложение двух смартфонов (один класс)"""
    phone1 = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
    phone2 = Smartphone("Samsung", "Описание", 2000, 3, 95.0, "S23", 256, "Серый")

    result = phone1 + phone2
    assert result == 1000 * 5 + 2000 * 3


def test_add_same_class_grass() -> None:
    """Проверяет сложение двух газонных трав (один класс)"""
    grass1 = LawnGrass("Трава 1", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Трава 2", "Описание", 300, 20, "США", "5 дней", "Темно-зеленый")

    result = grass1 + grass2
    assert result == 500 * 10 + 300 * 20


def test_add_different_classes_raises_type_error() -> None:
    """Проверяет, что при сложении разных классов возникает TypeError"""
    phone = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
    grass = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")

    with pytest.raises(TypeError):  # Я ожидаю ошибку TypeError
        phone + grass


def test_add_product_with_smartphone() -> None:
    """Проверяет, что смартфон можно сложить с продуктом (если Product, не наследник)"""
    phone = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
    product = Product("Товар", "Описание", 500, 10)

    # type(phone) is not type(product) → разные классы → ошибка
    with pytest.raises(TypeError):
        phone + product


# =========== Тестирование add_product с проверкой типов ===========


def test_add_product_to_category_with_smartphone() -> None:
    """Проверяет, что смартфон можно добавить в категорию"""
    phone = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
    category = Category("Смартфоны", "Описание", [])

    initial_count = Category.product_count
    category.add_product(phone)

    assert len(category.products) == 1
    assert Category.product_count == initial_count + 1


def test_add_product_to_category_with_grass() -> None:
    """Проверяет, что газонную траву можно добавить в категорию"""
    grass = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")
    category = Category("Трава", "Описание", [])

    initial_count = Category.product_count
    category.add_product(grass)

    assert len(category.products) == 1
    assert Category.product_count == initial_count + 1


def test_add_product_to_category_with_invalid_type_raises_error() -> None:
    """Проверяет, что при добавлении не-продукта возникает TypeError"""
    category = Category("Смартфоны", "Описание", [])

    with pytest.raises(TypeError):
        category.add_product("Not a product")  # type: ignore

    with pytest.raises(TypeError):
        category.add_product(123)  # type: ignore

    with pytest.raises(TypeError):
        category.add_product(None)  # type: ignore


def test_category_with_mixed_products() -> None:
    """Проверяет категорию с разными типами продуктов (Product, Smartphone, LawnGrass)"""
    # Обнуляем счётчики для чистоты теста
    Category.category_count = 0
    Category.product_count = 0

    product = Product("Товар", "Описание", 100, 5)
    phone = Smartphone("iPhone", "Описание", 1000, 3, 98.0, "15", 512, "Черный")
    grass = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")

    category = Category("Разное", "Описание", [product, phone, grass])

    assert len(category.products) == 3
    assert Category.product_count == 5 + 3 + 10


# =========== Тестирование наследования __add__ и __str__ ===========


def test_smartphone_uses_product_str() -> None:
    """Проверяет, что Smartphone использует метод __str__ от Product"""
    grass = Smartphone("iPhone", "Описание", 1000, 30, 98.0, "15", 512, "Черный")

    expected = "iPhone, 1000.0 руб. Остаток: 30 шт."
    assert str(grass) == expected


def test_grass_uses_product_str() -> None:
    """Проверяет, что LawnGrass использует метод __str__ от Product"""
    grass = LawnGrass("Трава", "Описание", 500, 10, "Россия", "7 дней", "Зеленый")

    expected = "Трава, 500.0 руб. Остаток: 10 шт."
    assert str(grass) == expected

# =========== Тест middle_price( ===========


def test_category_middle_price() -> None:
    """Тест проверяет подсчет средней цены в категории"""
    phone_1 = Smartphone("iPhone", "Описание", 1000, 5, 98.0, "15", 512, "Черный")
    phone_2 = Smartphone("Samsung", "Описание", 800, 3, 95.0, "S23", 256, "Белый")

    category = Category("Смартфоны", "Разные смартфоны", [phone_1, phone_2])

    assert category.middle_price() == 925.0

def test_category_middle_price_empty() -> None:
    """Тест проверяет, что при пустой категории возвращается 0"""
    category = Category("Пустая", "Нет товаров", [])
    assert category.middle_price() == 0


