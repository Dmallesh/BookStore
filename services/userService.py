from builtins import Exception

from flask_restful import marshal_with, fields

from models.bookstoremodels import User, WishList
from repositories import userRepository, wishlistRepository

user_resource_fields = {
    'pkUserId': fields.Integer,
    'sFirstName': fields.String,
    'sLastName': fields.String,
    'sEmail': fields.String,
    'sPassword': fields.String
}

wishlist_resource_fields = {
    'pkWishListId': fields.Integer,
    'fkUserId': fields.Integer,
    'fkBookId': fields.Integer,
    'sTitle': fields.String,
    'sAuthor': fields.String,
    'sISBN': fields.String,
    'dtPublished': fields.String
}

class UserService():
    def __init__(self):
        self.userRepo = userRepository.UserRepository()
        self.wishlistRepo = wishlistRepository.WishListRepository()


    @marshal_with(user_resource_fields)
    def getAllUser(self):
        data =  self.userRepo.get_all_users()
        if data == None:
            raise ValueError("No records found!")

        return [User(*x) for x in data]


    @marshal_with(user_resource_fields)
    def getUser(self, pkUserId):
        data =  self.userRepo.get_user(pkUserId)
        if data == None:
            raise ValueError("User not found!")

        return User(*data)

    def addUser(self, user):
        return self.userRepo.add_user(user)

    def deleteUser(self, pkUserId):
        data = self.userRepo.get_user(pkUserId)
        if data == None:
            raise ValueError("No records found!")

        return self.userRepo.delete_user(pkUserId)

    def updateUser(self, pkUserId, user):
        data = self.userRepo.get_user(pkUserId)
        if data == None:
            raise ValueError("No records found!")

        return self.userRepo.update_user(pkUserId, user)
