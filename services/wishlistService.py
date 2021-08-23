from flask_restful import marshal_with, fields
from models.bookstoremodels import WishList
from repositories import wishlistRepository, userRepository , bookRepository


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
        self.userRepo = userRepository.UserRepository()
        self.bookRepo = bookRepository.BookRepository()

    @marshal_with(wishlist_resource_fields)
    def getUserWishList(self, fkUserId):
        findUser = self.userRepo.get_user(fkUserId)
        if findUser == None:
            raise ValueError("User not found!")

        data = self.wishlistRepo.get_wishlist(fkUserId)
        return [WishList(*x) for x in data]

    @marshal_with(wishlist_resource_fields)
    def addBookToWishList(self, fkUserId, fkBookId):
        findUser = self.userRepo.get_user(fkUserId)
        if findUser == None:
            raise ValueError("User not found!")

        findBook = self.bookRepo.get_book(fkBookId)
        if findBook == None:
            raise ValueError("Book not found!")

        findWishList = self.wishlistRepo.get_wishlist_book_user(fkUserId, fkBookId)
        if findWishList != None:
            raise ValueError("Book is present in wishlist!")

        newrowid = self.wishlistRepo.add_wishlist(fkUserId, fkBookId)
        data = self.wishlistRepo.get_wishlist_Id(newrowid)
        return WishList(*data)

    def deleteBookFromWishList(self, fkUserId, fkBookId):
        findWishList = self.wishlistRepo.get_wishlist_book_user(fkUserId, fkBookId)
        if findWishList == None:
            raise ValueError("Book not present in wishlist!")

        return self.wishlistRepo.delete_book_wishlist(fkUserId, fkBookId)


    def deleteAllBookFromWishList(self, fkUserId):
        findUser = self.userRepo.get_user(fkUserId)
        if findUser == None:
            raise ValueError("User not found!")

        return self.wishlistRepo.delete_all_Book_wishlist(fkUserId)




