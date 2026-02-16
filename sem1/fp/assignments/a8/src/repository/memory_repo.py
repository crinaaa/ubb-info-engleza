from src.domain.domain import Book

class MemoryBookError(Exception):
    """
    Customized exception used for raising value errors.
    """
    pass


class BookMemoryRepository:
    """
    Class that handles the repository in the memory.
    """

    def __init__(self):
        """
        The constructor of the class.
        Saves the list of operations that have been performed, the ISBNs (unique identifiers) of the books
        (as a dictionary) and the exact order of the books in the collection.
        """
        self._data = {}     # isbns
        self._history = []  # undo stack
        self._order = []  # list of isbns in positional order

    def add(self, new_book: Book, can_add: bool) -> None:
        """
        Adds a new book to the collection of books.
        :rtype: None
        :param new_book: the book we wish to add (of type Book)
        :param can_add: boolean value, it tells us if we can add the operation to the history or not
        :raises ValueError: If a book with the same ISBN as the one given by the user already exists,
        the program raises an error.
        """
        if new_book.isbn in self._data:
            raise MemoryBookError("Book is already in this repo!")

        self._data[new_book.isbn] = new_book
        self._order.append(new_book.isbn)  # track order

        if can_add:
            self._history.append(["add", new_book.isbn])

    def get_all(self) -> list:
        """
        Returns the list of all current books, in their exact order.
        :return: the list of all current books
        :rtype: list
        """
        #return list(self._data.values())
        return [self._data[isbn] for isbn in self._order]


    def filter_title_start(self, word: str) -> None:
        """
        Filters the collection of books. Those whose title starts with a given word are removed.
        Chooses the books whose title does not start with the given word (treats it as lowercase), places them in a new dictionary,
        which becomes the new self._data.
        :rtype: None
        :param word: the word we want to use for filtering
        :return: the list of books whose title does not start
        """
        removed = []
        new_data = {}
        new_order = []

        # go through books in order
        for index, isbn in enumerate(self._order):
            book = self._data[isbn]

            if book.title.lower().startswith(word.lower()):
                removed.append((index, book))  # store old pos + book
            else:
                new_data[isbn] = book  # keep the book
                new_order.append(isbn)  # keep its pos

        self._data = new_data
        self._order = new_order

        # remember history for undo
        if removed:
            self._history.append(["filter", removed])


    def erase_data(self) -> None:
        """
        Deletes all the data from the repository. (Useful for testing.)
        :rtype: None
        """
        self._data.clear()
        self._order.clear()


    # called for the undo
    def delete_book(self, isbn: str) -> None:
        """
        Deletes a given book from the book collection.
        :rtype: None
        """
        if isbn in self._order:
            self._order.remove(isbn)
        if isbn in self._data:
            del self._data[isbn]


    def undo(self) -> None:
        """
        Undoes the last performed operation. If the last performed operation was "add", then it deletes
        a book. Otherwise, if the last performed operation was "filter", then it adds back the removed
        books.
        :rtype: None
        :raises ValueError: If there isn't any other action to undo, the program raises an error.
        """
        if not self._history:
            raise MemoryBookError("Cannot undo anymore!")

        operation = self._history.pop()   #get the last operation
        op_type = operation[0]

        if op_type == "filter":
            # restore removed books at original positions
            removed = operation[1]
            for index, book in removed:
                self._data[book.isbn] = book
                self._order.insert(index, book.isbn)

        elif op_type == "add":
            # delete book
            isbn = operation[1]
            self.delete_book(isbn)

        else:
            raise MemoryBookError("Unknown operation type.")