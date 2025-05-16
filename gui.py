from PyQt5 import QtWidgets, QtCore, QtGui
from domain import Book, EBook, DigitalLibrary

class LibraryGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.library = DigitalLibrary()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setFixedSize(700, 420)
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 18, 20, 12)

        # Header
        header = QtWidgets.QLabel("Library Management System")
        header.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        main_layout.addWidget(header)

        # Form Grid
        form_grid = QtWidgets.QGridLayout()
        form_grid.setVerticalSpacing(8)
        form_grid.setHorizontalSpacing(10)

        form_grid.addWidget(QtWidgets.QLabel("Title:"), 0, 0)
        self.title_entry = QtWidgets.QLineEdit()
        form_grid.addWidget(self.title_entry, 0, 1)

        form_grid.addWidget(QtWidgets.QLabel("Author:"), 1, 0)
        self.author_entry = QtWidgets.QLineEdit()
        form_grid.addWidget(self.author_entry, 1, 1)

        form_grid.addWidget(QtWidgets.QLabel("ISBN:"), 2, 0)
        self.isbn_entry = QtWidgets.QLineEdit()
        form_grid.addWidget(self.isbn_entry, 2, 1)

        self.ebook_checkbox = QtWidgets.QCheckBox("eBook")
        self.ebook_checkbox.stateChanged.connect(self.toggle_ebook)
        form_grid.addWidget(self.ebook_checkbox, 0, 2)

        form_grid.addWidget(QtWidgets.QLabel("Size (MB):"), 1, 2)
        self.size_entry = QtWidgets.QLineEdit()
        self.size_entry.setEnabled(False)
        self.size_entry.setValidator(QtGui.QDoubleValidator(0.1, 9999, 2))
        form_grid.addWidget(self.size_entry, 1, 3)

        # Buttons
        self.add_btn = QtWidgets.QPushButton("Add Book")
        self.add_btn.clicked.connect(self.add_book)
        form_grid.addWidget(self.add_btn, 3, 1)

        self.lend_btn = QtWidgets.QPushButton("Lend Book")
        self.lend_btn.clicked.connect(self.lend_book)
        form_grid.addWidget(self.lend_btn, 3, 2)

        self.return_btn = QtWidgets.QPushButton("Return Book")
        self.return_btn.clicked.connect(self.return_book)
        form_grid.addWidget(self.return_btn, 3, 3)

        main_layout.addLayout(form_grid)

        # Available Books Table
        main_layout.addSpacing(10)
        self.table = QtWidgets.QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", "Type", "Size/MB"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setFixedHeight(180)
        main_layout.addWidget(QtWidgets.QLabel("Available Books:"))
        main_layout.addWidget(self.table)

        # Author filter
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel("Filter by Author:"))
        self.author_filter_entry = QtWidgets.QLineEdit()
        filter_layout.addWidget(self.author_filter_entry)
        self.filter_btn = QtWidgets.QPushButton("Filter")
        self.filter_btn.clicked.connect(self.filter_by_author)
        filter_layout.addWidget(self.filter_btn)
        self.showall_btn = QtWidgets.QPushButton("Show All")
        self.showall_btn.clicked.connect(self.display_books)
        filter_layout.addWidget(self.showall_btn)
        main_layout.addLayout(filter_layout)

        # Initial books
        self.library.add_book(Book("Python Fundamentals", "Ali", "111111"))
        self.library.add_book(Book("Object-Oriented Programming", "Shehroz", "222222"))
        self.library.add_book(Book("Data Science Essentials", "Ali", "333333"))
        self.library.add_ebook(EBook("Machine Learning Guide", "Shehroz", "444444", 10))
        self.display_books()

    def toggle_ebook(self, state):
        if self.ebook_checkbox.isChecked():
            self.size_entry.setEnabled(True)
        else:
            self.size_entry.clear()
            self.size_entry.setEnabled(False)

    def add_book(self):
        title = self.title_entry.text().strip()
        author = self.author_entry.text().strip()
        isbn = self.isbn_entry.text().strip()
        is_ebook = self.ebook_checkbox.isChecked()
        size = self.size_entry.text().strip()

        if not title or not author or not isbn:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        if is_ebook:
            if not size:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Please enter download size for eBook.")
                return
            try:
                size_val = float(size)
                if size_val <= 0:
                    raise ValueError
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Input Error", "Download size must be a positive number.")
                return
            book = EBook(title, author, isbn, size_val)
            self.library.add_ebook(book)
        else:
            book = Book(title, author, isbn)
            self.library.add_book(book)

        self.display_books()
        self.title_entry.clear()
        self.author_entry.clear()
        self.isbn_entry.clear()
        self.size_entry.clear()
        self.ebook_checkbox.setChecked(False)
        self.size_entry.setEnabled(False)

    def lend_book(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            QtWidgets.QMessageBox.information(self, "Select Book", "Please select a book to lend.")
            return
        row = rows[0].row()
        isbn = self.table.item(row, 2).text()
        try:
            msg = self.library.lend_book(isbn)
            QtWidgets.QMessageBox.information(self, "Success", msg)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
        self.display_books()

    def return_book(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            QtWidgets.QMessageBox.information(self, "Select Book", "Please select a book to return.")
            return
        row = rows[0].row()
        isbn = self.table.item(row, 2).text()
        msg = self.library.return_book(isbn)
        QtWidgets.QMessageBox.information(self, "Returned", msg)
        self.display_books()

    def display_books(self):
        self.table.setRowCount(0)
        for book in self.library.available_books():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(book.title))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(book.author))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(book.isbn))
            if isinstance(book, EBook):
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem("eBook"))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(book.download_size)))
            else:
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem("Book"))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem("-"))

    def filter_by_author(self):
        author = self.author_filter_entry.text().strip()
        if not author:
            QtWidgets.QMessageBox.information(self, "Enter Author", "Please specify an author name.")
            return
        filtered = self.library.books_by_author(author)
        self.table.setRowCount(0)
        for book in filtered:
            if book.is_available:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(book.title))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(book.author))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(book.isbn))
                if isinstance(book, EBook):
                    self.table.setItem(row, 3, QtWidgets.QTableWidgetItem("eBook"))
                    self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(book.download_size)))
                else:
                    self.table.setItem(row, 3, QtWidgets.QTableWidgetItem("Book"))
                    self.table.setItem(row, 4, QtWidgets.QTableWidgetItem("-"))