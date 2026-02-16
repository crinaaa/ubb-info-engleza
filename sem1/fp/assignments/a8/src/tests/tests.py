from src.services.services import BookService
from src.repository.json_file_repo import JsonFileRepo
from src.repository.memory_repo import BookMemoryRepository
from src.repository.text_file_repo import TextFileRepository
from src.repository.binary_file_repo import BinaryFileRepo

class Test:
    def __init__(self, repo):
        # initialize the service with the repo
        self.book_service = BookService(repo)

    def test_random_values(self):
        # after generating random books, we should have exactly 10
        self.book_service.generate_random_books()
        assert len(self.book_service.get_all_books()) == 10

    def test_add(self):
        # add a new book
        self.book_service.add_book("1234", "Alice", "Python 101", True)
        assert len(self.book_service.get_all_books()) == 11

        # add another new book
        self.book_service.add_book("5678", "Bob", "Data Science", True)
        assert len(self.book_service.get_all_books()) == 12

        # try adding a duplicate isbn – shouldn't increase length
        try:
            self.book_service.add_book("1234", "Charlie", "Deep Learning", True)
        except Exception:
            pass
        assert len(self.book_service.get_all_books()) == 12

    def test_all_repositories(self):

        memo_repo_test = BookMemoryRepository()
        text_repo_test = TextFileRepository("books_test.txt")
        bin_repo_test = BinaryFileRepo("books_test.bin")
        json_repo_test = JsonFileRepo("books_test.json")

        memo_repo_test.erase_data()
        tests_memory_repository = Test(memo_repo_test)
        tests_memory_repository.test_all()

        text_repo_test.erase_data()
        tests_memory_repository = Test(text_repo_test)
        tests_memory_repository.test_all()

        bin_repo_test.erase_data()
        tests_memory_repository = Test(bin_repo_test)
        tests_memory_repository.test_all()

        json_repo_test.erase_data()
        tests_memory_repository = Test(json_repo_test)
        tests_memory_repository.test_all()

    def test_all(self):
        self.test_random_values()
        self.test_add()
        #print("All book tests passed successfully!")
