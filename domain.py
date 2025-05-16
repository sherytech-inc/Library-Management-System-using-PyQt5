class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class EBook(Book):
    def __init__(self, title, author, isbn, download_size):
        super().__init__(title, author, isbn)
        self.download_size = download_size

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}, Size: {self.download_size} MB)"

class DigitalLibrary:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def add_ebook(self, ebook):
        self.books.append(ebook)

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.is_available:
                    book.is_available = False
                    return f"Book '{book.title}' is lent."
                else:
                    raise Exception(f"Book '{book.title}' is not available!")
        return "Book not found!"

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.is_available = True
                return f"Book '{book.title}' returned."
        return "Book not found!"

    def available_books(self):
        return [book for book in self.books if book.is_available]

    def books_by_author(self, author):
        return [book for book in self.books if book.author == author]