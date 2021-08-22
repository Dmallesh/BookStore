from flask import json
class User():
    def __init__(self,pkUserId, sFirstName, sLastName, sEmail, sPassword):
        self.pkUserId = pkUserId
        self.sFirstName = sFirstName
        self.sLastName = sLastName
        self.sEmail = sEmail
        self.sPassword = sPassword

class Book():
    def __init__(self,pkBookId,sTitle, sAuthor, sISBN, dtPublished):
        self.pkBookId = pkBookId
        self.sTitle = sTitle
        self.sAuthor = sAuthor
        self.sISBN = sISBN
        self.dtPublished = dtPublished


class WishList():
    def __init__(self, pkWishListId, fkUserId, fkBookId,sTitle, sAuthor, sISBN, dtPublished):
        self.pkWishListId = pkWishListId
        self.fkUserId = fkUserId
        self.fkBookId = fkBookId
        self.sTitle = sTitle
        self.sAuthor = sAuthor
        self.sISBN = sISBN
        self.dtPublished = dtPublished


class ErrorReponse(Exception):
    def __init__(self, internalLog, externalLog, errorCode, statusCode):
        self.internalLog = internalLog
        self.externalLog = externalLog
        self.errorcode = errorCode
        self.statuscode = statusCode