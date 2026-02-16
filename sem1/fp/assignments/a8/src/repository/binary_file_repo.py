from time import sleep

from src.domain.domain import Book
from src.repository.memory_repo import BookMemoryRepository
import pickle

class BinaryFileRepo(BookMemoryRepository):
    """
    Class that handles the repository in a binary file (it's information is intended to be read by the
    computer, thus it's not written in natural language). It inherits from the BookMemoryRepository class.
    """

    def __init__(self, file_name = "books.bin"):
        """
        The constructor of the class. It saves the file's name and loads the file, that is,
        it reads the information from the text file.
        :param file_name: the name of the file where we store the information
        """
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self) -> None:
        """
        Loads all the books from the text file. It does not record undo history, because we cannot
        modify these books.
        :rtype: None
        """
        try:
            fin = open(self._file_name, "rb")
            obj = pickle.load(fin)
        except EOFError:
            return

        for new_book in obj:
            super().add(new_book, False)

        fin.close()

    def _save_file(self) -> None:
        """
        It saves all the books to the given text file.
        :rtype: None
        """
        fout = open(self._file_name, "wb")
        pickle.dump(self.get_all(), fout)

        fout.close()

    def erase_data(self) -> None:
        """
        Deletes all the data from the repository. (Useful for testing.)
        Overrides the method from the memory repository, in order to adapt it to the file format.
        :rtype: None
        """
        super().erase_data()
        open(self._file_name, "w").close()

    #overwrite functions
    def add(self, new_book: Book, can_add: bool) -> None:
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

    def filter_title_start(self, word: str) -> None:
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

    def undo(self) -> None:
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