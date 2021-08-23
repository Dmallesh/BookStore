from datacontext import bookstoreContext

INSERT_WISHLIST = 'insert into tblWishList( fkUserId, fkBookId) values (?,?)'
SELECT_WISHLIST_USER = 'select pkWishListId,fkUserId, fkBookId, sTitle, sAuthor, sISBN, dtPublished  from ' \
                       'tblWishList inner join tblBook on pkBookId = fkBookId where fkUserId = ?'
DELETE_BOOK_WISHLIST = 'delete from tblWishList where fkUserId = ? and fkBookId = ?'
DELETE_ALL_BOOK_WISHLIST = 'delete from tblWishList where fkUserId = ?'
SELECT_WISHLIST_BOOK_USER = 'select pkWishListId ' \
                            ' from tblWishList where fkUserId = ? and fkBookId = ?'
SELECT_WISHLIST_ID = 'select pkWishListId,fkUserId, fkBookId, sTitle, sAuthor, sISBN, dtPublished  from ' \
                       'tblWishList inner join tblBook on pkWishListId = ?'

class WishListRepository():
    def __init__(self):
        self.db =bookstoreContext.connection()
        self.cursor = self.db.cursor()

    def get_wishlist(self,fkUserId):
        return self.cursor.execute(SELECT_WISHLIST_USER,(fkUserId,)).fetchall()

    def get_wishlist_book_user(self, fkUserId, fkBookId):
        return self.cursor.execute(SELECT_WISHLIST_BOOK_USER, (fkUserId, fkBookId,)).fetchone()

    def get_wishlist_Id(self, pkWishListId):
        return self.cursor.execute(SELECT_WISHLIST_ID, (pkWishListId,)).fetchone()

    def add_wishlist(self,fkUserId, fkBookId):
        self.cursor.execute(INSERT_WISHLIST,(fkUserId, fkBookId,  ))
        rowid = self.cursor.lastrowid
        self.db.commit()
        return rowid

    def delete_book_wishlist(self, fkUserId, fkBookId):
        self.cursor.execute(DELETE_BOOK_WISHLIST, (fkUserId, fkBookId,))
        self.db.commit()

    def delete_all_Book_wishlist(self, fkUserId):
        self.cursor.execute(DELETE_ALL_BOOK_WISHLIST, (fkUserId,))
        self.db.commit()

