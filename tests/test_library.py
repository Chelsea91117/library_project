import unittest
from unittest.mock import patch, mock_open
from library import Library
from book import Book


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.mock_storage = "test_storage.json"
        self.library = Library(storage_file=self.mock_storage)

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_load_books_empty(self, mock_file):
        """Тест, когда файл содержит пустой список книг"""
        books = self.library.load_books()
        self.assertEqual(books, [])
        mock_file.assert_called_once_with(self.mock_storage, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open,
           read_data='[{"id": 1, "title": "Book 1", "author": "Author 1", "year": 2021, "status": "в наличии"}, \
           {"id": 2, "title": "Book 2", "author": "Author 2", "year": 2022, "status": "в наличии"}]')
    def test_load_books_non_empty(self, mock_file):
        """Тест, когда файл содержит список из двух книг"""
        books = self.library.load_books()
        expected_books = [
            {"id": 1, "title": "Book 1", "author": "Author 1", "year": 2021, "status": "в наличии"},
            {"id": 2, "title": "Book 2", "author": "Author 2", "year": 2022, "status": "в наличии"}
        ]
        # Преобразуем загруженные книги в словари для сравнения
        books_as_dicts = [book.to_dict() for book in books]
        self.assertEqual(books_as_dicts, expected_books)
        mock_file.assert_called_once_with(self.mock_storage, "r", encoding="utf-8")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_books(self, mock_json_dump, mock_file):
        """Тест проверяет корректную запись данных в файл"""
        self.library.books = [
            Book(1, "Test Book", "Test Author", 2023, "в наличии")
        ]
        self.library.save_books()
        mock_file.assert_called_once_with(self.mock_storage, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(
            [book.to_dict() for book in self.library.books],
            mock_file(),
            ensure_ascii=False,
            indent=4,
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_books_io_error(self, mock_json_dump, mock_file):
        """Тест на проверку ошибки ввода-вывода при записи в файл."""
        self.library.books = [Book(1, "Test Book", "Test Author", 2023, "в наличии")]
        mock_file.side_effect = IOError("Error writing to file")
        with self.assertRaises(IOError):
            self.library.save_books()
        mock_file.assert_called_once_with(self.mock_storage, "w", encoding="utf-8")
        mock_json_dump.assert_not_called()

    def test_add_book(self):
        """Тест проверяет, что новый объект книги создается с правильными атрибутами"""
        with patch("library.Library.save_books"):
            new_book = self.library.add_book("New Book", "Author", 2023)
        self.assertEqual(new_book.title, "New Book")
        self.assertEqual(new_book.author, "Author")
        self.assertEqual(new_book.year, 2023)
        self.assertEqual(new_book.status, "в наличии")

    def test_find_book_by_id(self):
        """
        Тест проверяет, что книга с ID 1 найдена правильно,
        а при поиске книги с несуществующим ID выбрасывается исключение
        """
        self.library.books = [
            Book(1, "Book1", "Author1", 2023, "в наличии"),
            Book(2, "Book2", "Author2", 2022, "выдана"),
        ]
        book = self.library.find_book_by_id(1)
        self.assertEqual(book.title, "Book1")

        with self.assertRaises(ValueError):
            self.library.find_book_by_id(99)

    def test_remove_book(self):
        """
        Тест проверяет, что книга с ID 1 успешно удалена успешно,
        а при удалении книги с несуществующим ID выбрасывается исключение
        """
        library = Library("test_storage.json")
        book1 = Book(1, "Book 1", "Author 1", 2001, "в наличии")
        book2 = Book(2, "Book 2", "Author 2", 2002, "в наличии")
        library.books = [book1, book2]

        library.remove_book(1)
        self.assertEqual(len(library.books), 1)
        self.assertNotIn(book1, library.books)

        with self.assertRaises(ValueError):
            library.remove_book(99)

    def test_search_books(self):
        """
        Тест проверяет, что поиск книги по заголовку Python успешен,
        поиск книги по автору Author2 успешен,
        поиск книги по году 2023 успешен,
        а поиск по несуществующему параметру выдает пустой словарь
        """
        self.library.books = [
            Book(1, "Python Programming", "Author1", 2023, "в наличии"),
            Book(2, "Data Science", "Author2", 2022, "выдана"),
            Book(3, "Learn Python", "Author3", 2023, "в наличии"),
        ]
        results = self.library.search_books("Python")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].title, "Python Programming")

        results = self.library.search_books("Author2")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Data Science")

        results = self.library.search_books("2023")
        self.assertEqual(len(results), 2)

        results = self.library.search_books("2025")
        self.assertEqual(results, [])

    def test_list_books(self):
        """Тест проверяет, что метод корректно возвращает список книг, когда в библиотеке есть хотя бы одна книга."""
        self.library.books = [
            Book(1, "Book1", "Author1", 2023, "в наличии"),
        ]
        books = self.library.list_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Book1")

    def test_list_books_empty(self):
        """Тест проверяет, что метод корректно обрабатывает случай, когда в библиотеке нет книг."""
        self.library.books = []
        books = self.library.list_books()
        self.assertEqual(len(books), 0)

    def test_update_status(self):
        """
        Тест проверяет, успешное обновление статуса,
        повторное обновление статуса,
        обработку недопустимого значения статуса
        """
        self.library.books = [
            Book(1, "Book1", "Author1", 2023, "в наличии"),
        ]
        with patch("library.Library.save_books"):
            updated = self.library.update_status(self.library.books[0], "выдана")
        self.assertTrue(updated)
        self.assertEqual(self.library.books[0].status, "выдана")

        with patch("library.Library.save_books"):
            updated = self.library.update_status(self.library.books[0], "выдана")
        self.assertFalse(updated)

        with self.assertRaises(ValueError):
            self.library.update_status(self.library.books[0], "недоступна")

    def test_display_books(self):
        """
        Тест проверяет отображение списка книг,
        отображение пустого списка книг
        """
        self.library.books = [
            Book(1, "Book1", "Author1", 2023, "в наличии"),
        ]
        with patch("builtins.print") as mock_print:
            self.library.display_books(self.library.books)
        mock_print.assert_called_with(self.library.books[0])

        with patch("builtins.print") as mock_print:
            self.library.display_books([])
        mock_print.assert_called_with("Список книг пуст.")


