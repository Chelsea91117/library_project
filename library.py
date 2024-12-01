from book import Book
import json
from typing import List

class Library:
    def __init__(self, storage_file: str = "storage.json"):
        self.storage_file = storage_file
        self.books: List[Book] = self.load_books()

    # Загрузка данных из файла
    def load_books(self) -> List[Book]:
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except FileNotFoundError:
            return []
        except json.decoder.JSONDecodeError:
            raise ValueError("Ошибка при чтении файла хранения данных.")
        except Exception as e:
            raise ValueError(f"Неизвестная ошибка: {e}")

    # Сохранение данных в файл
    def save_books(self) -> None:
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    # Добавление новой книги
    def add_book(self, title: str, author: str, year: int) -> Book:
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(id=new_id, title=title, author=author, year=year, status = "в наличии")
        self.books.append(new_book)
        self.save_books()
        return new_book

    # Поиск книги по id
    def find_book_by_id(self, book_id: int) -> Book:
        if not isinstance(book_id, int) or book_id < 1:
            raise ValueError("ID книги должен быть положительным числом.")
        try:
            current_book = next(book for book in self.books if book.id == book_id)
            print(current_book)
            return current_book
        except StopIteration:
            raise ValueError(f"Книга с ID {book_id} не найдена.")

    # Удаление книги
    def remove_book(self, book_id: int) -> None:
        try:
            book = self.find_book_by_id(book_id)
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} успешно удалена!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    # Поиск книг по названию, автору и году
    def search_books(self, query: str) -> List[Book]:
        results = [
            book for book in self.books
            if query.lower() in book.title.lower()
               or query.lower() in book.author.lower()
               or query == str(book.year)
        ]
        return results

    # Отображение всех книг
    def list_books(self) -> List[Book]:
        if not self.books:
            print("Список книг пуст.")
        return self.books

    # Обновление статуса
    def update_status(self, book: Book, status: str) -> bool:
        status = status.strip()

        # Проверка корректности статуса
        if status not in Book.ALLOWED_STATUSES:
            print("Ошибка: недопустимый статус. Статус должен быть 'в наличии' или 'выдана'.")
            return False

        # Сохранение в случае измененного статуса
        if book.status != status:
            book.status = status
            self.save_books()
            print("Статус успешно обновлён.")
            return True
        else:
            print("Статус не изменился, так как он уже установлен.")
            return False

    # Вывод списка книг
    @staticmethod
    def display_books(books: List[Book]) -> None:
        if not books:
            print("Список книг пуст.")
        else:
            for book in books:
                print(book)
