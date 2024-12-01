import unittest
from book import Book


class TestBook(unittest.TestCase):

    def test_book_creation_valid(self):
        """Тест на корректное создание книги."""
        book = Book(id=1, title="Python 101", author="John Doe", year=2020, status="в наличии")
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Python 101")
        self.assertEqual(book.author, "John Doe")
        self.assertEqual(book.year, 2020)
        self.assertEqual(book.status, "в наличии")

    def test_invalid_id(self):
        """Тест на создание книги с некорректным ID."""
        with self.assertRaises(ValueError) as context:
            Book(id=-1, title="Invalid Book", author="Author", year=2020, status="в наличии")
        self.assertEqual(str(context.exception), "ID книги должен быть неотрицательным целым числом.")

    def test_invalid_status(self):
        """Тест на создание книги с некорректным статусом."""
        with self.assertRaises(ValueError) as context:
            Book(id=1, title="Invalid Status Book", author="Author", year=2020, status="неизвестно")
        expected_message = f"Недопустимый статус книги: неизвестно. " \
                           f"Допустимые значения: {Book.ALLOWED_STATUSES}"
        self.assertEqual(str(context.exception), expected_message)

    def test_invalid_title(self):
        """Тест на создание книги с некорректным заголовком."""
        with self.assertRaises(TypeError) as context:
            Book(id=1, title=123, author="Author", year=2020, status="в наличии")
        self.assertEqual(str(context.exception), "Название книги должно быть строкой.")

    def test_to_dict(self):
        """Тест на преобразование книги в словарь."""
        book = Book(id=1, title="Python 101", author="John Doe", year=2020, status="в наличии")
        expected_dict = {
            "id": 1,
            "title": "Python 101",
            "author": "John Doe",
            "year": 2020,
            "status": "в наличии"
        }
        self.assertEqual(book.to_dict(), expected_dict)

    def test_from_dict(self):
        """Тест на создание книги из словаря."""
        data = {
            "id": 1,
            "title": "Python 101",
            "author": "John Doe",
            "year": 2020,
            "status": "в наличии"
        }
        book = Book.from_dict(data)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Python 101")
        self.assertEqual(book.author, "John Doe")
        self.assertEqual(book.year, 2020)
        self.assertEqual(book.status, "в наличии")
