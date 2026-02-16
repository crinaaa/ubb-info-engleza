import random
from src.domain.domain import Book

class BookService:
    def __init__(self, repo):
        self._repo = repo
        #self.generate_random_books()

    def generate_random_books(self):
        """
        Generates 10 random books at startup with unique titles, unique authors, and unique ISBNs.
        These are not recorded in undo history.
        """

        titles = [
            "Python Basics", "Harry Potter", "Data Science", "Deep Learning",
            "Algorithms", "Machine Learning", "Cooking 101", "Gardening",
            "History of Art", "Space Exploration"
        ]
        authors = [
            "Alice Brown", "Bob Mike", "Charlie Dawson", "David Joe", "Eve Ally",
            "Frank Bitter", "Grace Hank", "Hannah Pattinson", "Ivan Koln", "Jack Black"
        ]

        # shuffle titles and authors
        random.shuffle(titles)
        random.shuffle(authors)

        used_isbns = set()

        for i in range(10):
            # ensure unique ISBN
            while True:
                isbn = str(random.randint(1000, 9999))
                if isbn not in used_isbns:
                    used_isbns.add(isbn)
                    break

            title = titles[i]
            author = authors[i]

            self.add_book(isbn, author, title, False)

    def get_all_books(self):
        return self._repo.get_all()

    def generate_if_empty(self):
        if len(self.get_all_books()) == 0:
            self.generate_random_books()

    def add_book(self, isbn: str, author: str, title: str, can_add: bool) -> None:
        """
        Adds a new book to the collection of books.
        :rtype: None
        :param isbn: the ISBN of the book
        :param author: the author of the book
        :param title: the title of the book
        :param can_add: boolean value that tells us if we can add the operation to the history or not
        """
        new_book = Book(isbn, author, title)
        self._repo.add(new_book, can_add)

    def filter_books(self, word: str):
        self._repo.filter_title_start(word)

    def undo(self):
        self._repo.undo()