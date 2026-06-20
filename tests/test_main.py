from typing import Any

import pytest

from src.main import Category, Product

# =========== Тестирование класса Product ===========


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
