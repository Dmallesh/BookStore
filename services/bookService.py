from flask_restful import marshal_with, fields

from models.bookstoremodels import Book
from repositories import bookRepository

resource_fields = {
    'pkBookId': fields.Integer,
    'sTitle': fields.String,
    'sAuthor': fields.String,
    'sISBN': fields.String,
    'dtPublished': fields.String
}


class BookService():
    def __init__(self):
        self.bookRepo = bookRepository.BookRepository()

    @marshal_with(resource_fields)
    def getAllBook(self):
        data =  self.bookRepo.get_all_books()
        if data == None:
            raise ValueError("No records found!")

        return [Book(*x) for x in data]


    @marshal_with(resource_fields)
    def getBook(self, pkBookId):
        data =  self.bookRepo.get_book(pkBookId)
        if data == None:
            raise ValueError("Book not found!")

        return Book(*data)

    def addBook(self, book):
        return self.bookRepo.add_book(book)

    def deleteBook(self, pkBookId):
        data = self.bookRepo.get_book(pkBookId)
        if data == None:
            raise ValueError("No records found!")

        return self.bookRepo.delete_book(pkBookId)

    def updateBook(self, pkBookId, book):
        data = self.bookRepo.get_book(pkBookId)
        if data == None:
            raise ValueError("No records found!")

        return self.bookRepo.update_book(pkBookId, book)
