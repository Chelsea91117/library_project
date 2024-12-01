from library import Library
from time import sleep

def main():
    library = Library()

    while True:
        border = "=" * 40
        print(f"""
{border}
    Добро пожаловать в библиотеку!
{border}
    Доступные команды:
    1. Показать все книги
    2. Поиск книги
    3. Добавить книгу
    4. Удалить книгу
    5. Изменить статус книги
    6. Выйти
{border}
""")

        choice = input("Введите номер команды: ")

        if choice == "1":
            books = library.list_books()
            library.display_books(books)
            sleep(3)

        elif choice == "2":
            query = input("Введите запрос для поиска: ")
            books = library.search_books(query)
            library.display_books(books)
            sleep(3)

        elif choice == "3":
            try:
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                book = library.add_book(title, author, year)
                print(f"Книга добавлена: {book}")
            except ValueError:
                print("Ошибка: Вы должны заполнить все поля корректно.")
            sleep(3)

        elif choice == "4":
            try:
                book_id = int(input("Введите ID книги: "))
                library.remove_book(book_id)
            except ValueError:
                print("Ошибка: ID должен быть числом.")
            sleep(3)

        elif choice == "5":
            try:
                book_id = int(input("Введите ID книги: "))
                book = library.find_book_by_id(book_id)
                status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                library.update_status(book, status)
            except ValueError as e:
                print(f"Ошибка: {e}")
            sleep(3)

        elif choice == "6":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Ошибка: Некорректная команда, попробуйте снова.")
            sleep(3)


if __name__ == "__main__":
    main()