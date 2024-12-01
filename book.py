class Book:
    ALLOWED_STATUSES = {"в наличии", "выдана"}

    def __init__(self, id: int, title: str, author: str, year: int, status: str):
        if not isinstance(id, int) or id < 0:
            raise ValueError("ID книги должен быть неотрицательным целым числом.")
        if not isinstance(title, str):
            raise TypeError("Название книги должно быть строкой.")
        if not isinstance(author, str):
            raise TypeError("Автор должен быть строкой.")
        if not isinstance(year, int):
            raise TypeError("Год издания должен быть целым числом.")
        if status not in self.ALLOWED_STATUSES:
            raise ValueError(f"Недопустимый статус книги: {status}. "
                             f"Допустимые значения: {self.ALLOWED_STATUSES}")

        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        return{
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Book":
        try:
            return Book(
                id=data["id"],
                title=data["title"],
                author=data["author"],
                year=data["year"],
                status=data["status"],
            )
        except KeyError as e:
            raise ValueError(f"Отсутствует необходимое поле: {e}")

    def __str__(self):
        return (f"ID: {self.id:<5} | "
                f"Название: {self.title:<30} | "
                f"Автор: {self.author:<20} | "
                f"Год: {self.year:<15} | "
                f"Статус: {self.status}")