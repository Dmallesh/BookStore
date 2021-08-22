from services import userService, bookService
from flask_restful import marshal_with, fields

from models.bookstoremodels import User, WishList
from repositories import wishlistRepository


wishlist_resource_fields = {
    'pkWishListId': fields.Integer,
    'fkUserId': fields.Integer,
    'fkBookId': fields.Integer,
    'sTitle': fields.String,
    'sAuthor': fields.String,
    'sISBN': fields.String,
    'dtPublished': fields.String
}

class WishListService():
    def __init__(self):
        self.wishlistRepo = wishlistRepository.WishListRepository()
        self.userSvc = userService.UserService()
        self.bookSvc = bookService.BookService()

    @marshal_with(wishlist_resource_fields)
    def getUserWishList(self, fkUserId):
        findUser = self.userSvc.getUser(fkUserId)
        if findUser == None:
            raise ValueError("User not found!")

        data = self.wishlistRepo.get_wishlist(fkUserId)
        return [WishList(*x) for x in data]


    def addBookToWishList(self, fkUserId, fkBookId):
        findUser = self.userSvc.getUser(fkUserId)
        if findUser == None:
            raise ValueError("User not found!")

        findBook = self.bookSvc.getBook(fkBookId)
        if findBook == None:
            raise ValueError("Book not found!")

        findWishList = self.wishlistRepo.check_book_exists_wishlist(fkUserId, fkBookId)
        if findWishList != None:
            raise ProcessLookupError("Book is present in wishlist ")

        return self.wishlistRepo.add_wishlist(fkUserId, fkBookId)


    def deleteBookFromWishList(self, fkUserId, fkBookId):
        findUser = self.userSvc.getUser(fkUserId)
        if findUser == None:
            raise ValueError("User not found!")

        findBook = self.bookSvc.getBook(fkBookId)
        if findBook == None:
            raise ValueError("Book not found!")


        return self.wishlistRepo.delete_book_wishlist(fkUserId, fkBookId)


    def deleteAllBookFromWishList(self, fkUserId):
        findUser = self.userSvc.getUser(fkUserId)
        if findUser == None:
            raise ValueError("User not found!")

        return self.wishlistRepo.delete_all_Book_wishlist(fkUserId)



