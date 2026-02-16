from src.services.services import BookService
from src.repository.memory_repo import MemoryBookError

class UI:
    def __init__(self, repo):
        self.__book_service = BookService(repo)

    def print_ui(self):
        while True:
            print("1. Add a book.")
            print("2. Display the list of all books.")
            print("3. Filter books by title. Books whose titles start with a given word are deleted.")
            print("4. Undo the last operation you have performed.")
            print("5. Exit the application")

            option = input("Choose your option: ")

            if option == "1":
                try:
                    isbn = input("What is the ISBN of the book? ")
                    if not isbn.isdigit():
                        raise ValueError("ISBN must contain digits only!")

                    author = input("Who is the author of the book? ")

                    # Author must contain only letters and spaces
                    if not author.replace(" ", "").isalpha():
                        raise ValueError("Author name cannot contain numbers or special characters!")

                    title = input("What is the title of the book? ")

                    # Title must contain only letters and spaces
                    if not title.replace(" ", "").isalpha():
                        raise ValueError("Title cannot contain numbers or special characters!")

                    try:
                        self.__book_service.add_book(isbn, author, title, True)
                    except MemoryBookError as ve:
                        print(ve)

                except ValueError as ve:
                    print(ve)


            elif option == "2":
                books = self.__book_service.get_all_books()
                for book in books:
                    print(book)

            elif option == "3":
                try:
                    word = input("What word do you want to use for filtering?")
                    if not word.isalpha():
                        raise ValueError("The word can contain only letters!")

                    self.__book_service.filter_books(word)
                    
                except ValueError as ve:
                    print(ve)

            elif option == "4":
                try:
                    self.__book_service.undo()
                except MemoryBookError as me:
                    print(me)

            elif option == "5":
                print("Exiting the program!")
                return

            else:
                print("Your input is not valid! Please try again!")