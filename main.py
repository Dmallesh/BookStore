from flask import Flask, jsonify, request
import json
from services import userService, bookService,wishlistService
from models.bookstoremodels import ErrorReponse, User, Book, WishList


app = Flask(__name__)
userSvc = userService.UserService()
bookSvc = bookService.BookService()
wishlistSvc = wishlistService.WishListService()

@app.errorhandler(ErrorReponse)
def handle_bad_request(error):
     response = dict(())
     response['errorcode'] = error.errorcode
     response['internalLog'] = error.internalLog
     response['externalLog'] = error.externalLog
     return jsonify(response), error.statuscode


@app.route('/')
def index():
    return 'Welcome to Book Store!'


################# WISH LIST API ##############################################

@app.route('/user/<int:id>/book',methods=['GET'])
def GetUserWishList(id):
    try:
        return jsonify(wishlistSvc.getUserWishList(id))
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 30001, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Get wish list failed!', 30002, 500)

@app.route('/user/<int:userid>/book/<int:bookid>',methods=['POST'])
def AddBookToUserWishList(userid, bookid):
    try:
        wishlistSvc.addBookToWishList(userid, bookid)
        return jsonify(wishlistSvc.getUserWishList(userid))
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 30003, 404)
    except ProcessLookupError as e:
        raise ErrorReponse(str(e), str(e), 30004, 400)
    except Exception as e:
        raise ErrorReponse(str(e), 'Adding book to wish list failed!', 30005, 500)


@app.route('/user/<int:userid>/book/<int:bookid>',methods=['DELETE'])
def DeleteBookFromUserWishList(userid, bookid):
    try:
        wishlistSvc.deleteBookFromWishList(userid, bookid)
        return jsonify(wishlistSvc.getUserWishList(userid))
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 30006, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Deleting book from wishlist failed!', 30007, 500)


@app.route('/user/<int:id>/book',methods=['DELETE'])
def EmptyWishList(id):
    try:
        wishlistSvc.deleteAllBookFromWishList(id)
        return jsonify(wishlistSvc.getUserWishList(id))
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 30008, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Empty wish list failed!', 30009, 500)


################# USER API ##############################################
@app.route('/users',methods=['GET'])
def GetUsers():
    try:
        return jsonify(userSvc.getAllUser())
    except Exception as e:
        raise ErrorReponse(str(e), 'Get all users failed!', 10001, 500)


@app.route('/user/<int:id>',methods=['GET'])
def GetUser(id):
    try:
        ret = userSvc.getUser(id)
        return jsonify(ret)
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 10002, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Get user failed!', 10003, 500)


@app.route('/user',methods=['POST'])
def AddUser():
    try:
        user = User(**json.loads(request.data))
        id = userSvc.addUser(user)
        return jsonify(userSvc.getUser(id))
    except Exception as e:
        raise ErrorReponse(str(e), 'Add user failed!', 10004, 500)


@app.route('/user/<int:id>',methods=['DELETE'])
def deleteUser(id):
    try:
        userSvc.deleteUser(id)
        return jsonify(userSvc.getAllUser())
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 10005, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Delete user failed!', 10006, 500)


@app.route('/user/<int:id>',methods=['PUT'])
def updateUser(id):
    try:
        user = User(**json.loads(request.data))
        userSvc.updateUser(id, user)
        return jsonify(userSvc.getUser(id))
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 10007, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Update user failed', 10008, 500)

################# BOOK API ##############################################

@app.route('/books',methods=['GET'])
def GetBooks():
    try:

        return jsonify(bookSvc.getAllBook())
    except Exception as e:
        raise ErrorReponse(str(e), 'Get all books failed!', 20001, 500)


@app.route('/book/<int:id>',methods=['GET'])
def GetBook(id):
    try:
        ret = bookSvc.getBook(id)
        return jsonify(ret)
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 30002, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Get book failed!', 30003, 500)


@app.route('/book',methods=['POST'])
def AddBook():
    try:
        book = Book(**json.loads(request.data))
        id = bookSvc.addBook(book)
        return jsonify(bookSvc.getBook(id))
    except Exception as e:
        raise ErrorReponse(str(e), 'Add book failed!', 30004, 500)


@app.route('/book/<int:id>',methods=['DELETE'])
def deleteBook(id):
    try:
        bookSvc.deleteBook(id)
        return jsonify(bookSvc.getAllBook())
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 30005, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Delete book failed!', 30006, 500)


@app.route('/book/<int:id>',methods=['PUT'])
def updateBook(id):
    try:
        book = Book(**json.loads(request.data))
        bookSvc.updateBook(id, book)
        return jsonify(bookSvc.getBook(id))
    except ValueError as e:
        raise ErrorReponse(str(e), str(e), 30007, 404)
    except Exception as e:
        raise ErrorReponse(str(e), 'Update book failed', 30008, 500)

if __name__ == "__main__":
    app.run()
