import json
from src.domain.domain import Book
from src.repository.memory_repo import BookMemoryRepository

class JsonFileRepo(BookMemoryRepository):
    def __init__(self, file_name = "books.json"):
        # call superclass constructor
        super().__init__()
        self._file_name = file_name
        self._empty_file = False
        self._init_file()
        self._load_file()

    def _init_file(self):
        """
        Ensure the JSON file exists and is not empty.
        If the file doesn't exist or is empty, create it with [].
        """
        try:
            with open(self._file_name, "r") as fin:
                content = fin.read().strip()
                if content == "":
                    raise ValueError("Empty file!")
        except (FileNotFoundError, ValueError):
            with open(self._file_name, "w") as fout:
                fout.write("[]")  # JSON empty list

    def _load_file(self):
        # loads all books from the JSON file
        try:
            with open(self._file_name, "r") as f:
                data = json.load(f)
        except (IOError, json.JSONDecodeError):
            data = []

        if not data:
            self._file_empty = True
            return

        self._file_empty = False

        for book_dict in data:
            new_book = Book(
                book_dict["isbn"],
                book_dict["author"],
                book_dict["title"]
            )
            super().add(new_book, False)  # do not record undo

    def _save_file(self):
        # save all books to the JSON file
        books_as_dicts = [
            {"isbn": book.isbn, "author": book.author, "title": book.title}
            for book in self.get_all()
        ]

        with open(self._file_name, "w") as f:
            json.dump(books_as_dicts, f, indent=4)

    def erase_data(self):
        super().erase_data()
        open(self._file_name, "w").close()

    # overwrite functions

    def add(self, new_book: Book, can_add: bool):
        super().add(new_book, can_add)
        self._save_file()

    def filter_title_start(self, word: str):
        super().filter_title_start(word)
        self._save_file()

    def undo(self):
        super().undo()
        self._save_file()