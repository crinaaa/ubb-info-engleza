from src.repository.memory_repo import BookMemoryRepository
from src.repository.text_file_repo import TextFileRepository
from src.repository.binary_file_repo import BinaryFileRepo
from src.repository.json_file_repo import JsonFileRepo
from src.services.services import BookService
from src.ui.ui import UI
from src.tests.tests import Test
from jproperties import Properties


def get_repo_from_properties():
    configs = Properties()

    with open('setting.properties', 'rb') as config_file:
        configs.load(config_file)

        repo_string = configs.get("REPO").data
        if repo_string == "Memory":
            return BookMemoryRepository()
        elif repo_string == "Text":
            return TextFileRepository("books.txt")
        elif repo_string == "Binary":
            return BinaryFileRepo("books.bin")
        elif repo_string == "JSON":
            return JsonFileRepo("books.json")
        else:
            raise ValueError("Unknown REPO type:")


def main():
    tester = Test(BookMemoryRepository())
    tester.test_all_repositories()

    try:
        repo = get_repo_from_properties()
        service = BookService(repo)
        service.generate_if_empty()
        ui = UI(repo)
        ui.print_ui()
    except ValueError as ve:
        print(ve)


if __name__ == "__main__":
    main()
