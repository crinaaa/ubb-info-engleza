from src.domain.domain import Book
from src.repository.memory_repo import BookMemoryRepository

class TextFileRepository(BookMemoryRepository):
    # inherits from BookMemoryRepository
    """
    Class that handles the repository in a text file. It inherits from BookMemoryRepository class.
    """
    
    def __init__(self, file_name = "books.txt") -> None:
        """
        The constructor of the class. It saves the file's name and loads the file, that is, it reads
        the information from the text file.
        :rtype: None
        :param file_name: the name of the file where we store the information
        """
        # call superclass constructor
        super().__init__()
        self._file_name = file_name
        self._file_empty = False
        self._load_file()     # read books from file


    def _load_file(self) -> None:
        """
        Loads all the books from the text file. It does not record undo history, because we cannot
        modify these books.
        :rtype: None
        """
        lines = []
        try:
            fin = open(self._file_name, "rt")
            lines = fin.readlines()
            fin.close()
        except IOError:
            lines = []

        if len(lines) == 0:
            # that is, if the file is empty
            self._file_empty = True
            return

        self._file_empty = False

        for line in lines:
            current_line = line.split(",")
            # for each line : "isbn, author, title"
            new_book = Book(current_line[0].strip(), current_line[1].strip(), current_line[2].strip())
            super().add(new_book, False)

    def _save_file(self) -> None:
        """
        It saves all the books to the given text file.
        :rtype: None
        """
        fout = open(self._file_name, "wt")

        for book in self.get_all():
            book_string = book.isbn + "," + book.author + "," + book.title + "\n"
            fout.write(book_string)

        # close the file
        fout.close()

    def erase_data(self):
        """
        Deletes all the data from the repository. (Useful for testing.)
        Overrides the method from the memory repository, in order to adapt it to the file format.
        :rtype: None
        """
        super().erase_data()
        open(self._file_name, "w").close()

    def add(self, new_book: Book, can_add: bool):
        """
        Adds a new book to the collection of books.
        Overrides the method from the memory repository, in order to be able to save the information to
        the text file.
        :rtype: None
        :param new_book: the book we wish to add (of type Book)
        :param can_add: boolean value, it tells us if we can add the operation to the history or not
        """
        super().add(new_book, can_add)
        self._save_file()

    def filter_title_start(self, word: str):
        """
        Filters the collection of books. Those whose title starts with a given word are removed.
        Chooses the books whose title does not start with the given word (treats it as lowercase), places them in a new dictionary,
        which becomes the new self._data.
        Overrides the method from the memory repository, in order to be able to save the information to
        the text file.
        :rtype: None
        :param word: the word we want to use for filtering
        :return: the list of books whose title does not start
        """
        super().filter_title_start(word)
        self._save_file()

    def undo(self):
        """
        Undoes the last performed operation. If the last performed operation was "add", then it deletes
        a book. Otherwise, if the last performed operation was "filter", then it adds back the removed
        books.
        Overrides the method from the memory repository, in order to be able to save the information to
        the text file.
        :rtype: None
        :raises ValueError: If there isn't any other action to undo, the program raises an error.
        """
        super().undo()
        self._save_file()