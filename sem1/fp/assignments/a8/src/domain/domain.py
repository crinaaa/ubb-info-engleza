class Book:
    def __init__(self, isbn: str, author: str, title: str):
        self.__isbn = isbn
        self.__author = author
        self.__title = title

    @property
    def isbn(self):
        return self.__isbn

    @property
    def author(self):
        return self.__author

    @property
    def title(self):
        return self.__title

    def __str__(self):
        return f"ISBN: {self.isbn}, Author: {self.author}, Title: {self.title}"