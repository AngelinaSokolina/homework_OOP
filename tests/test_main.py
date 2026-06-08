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


# =========== Тестирование класса Category ===========


@pytest.fixture()
def category_main(product_main: Product) -> Category:  # ← принимает товар из фикстуры
    return Category("Кисломолочные продукты", "Молоко, кефир, сыры", [product_main])


def test_category_init(category_main: Category) -> None:
    assert category_main.name == "Кисломолочные продукты"
    assert category_main.description == "Молоко, кефир, сыры"
    assert len(category_main.products) == 1
    assert category_main.products[0].name == "Молоко"


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


# =========== Тестирование классов Product, Category ===========


def test_product_count() -> None:
    """Проверяет увеличение счётчика продуктов"""
    initial = Category.product_count
    p1 = Product("Товар 1", "Описание", 100, 1)
    p2 = Product("Товар 2", "Описание", 200, 1)
    Category("Категория", "Описание", [p1, p2])
    assert Category.product_count == initial + 2
