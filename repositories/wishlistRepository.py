from datacontext import bookstoreContext

INSERT_WISHLIST = 'insert into tblWishList( fkUserId, fkBookId) values (?,?)'
SELECT_WISHLIST = 'select pkWishListId,fkUserId, fkBookId, sTitle, sAuthor, sISBN, dtPublished  from ' \
                       'tblWishList inner join tblBook on pkBookId = fkBookId where fkUserId = ?'
DELETE_BOOK_WISHLIST = 'delete from tblWishList where fkUserId = ? and fkBookId = ?'
DELETE_ALL_BOOK_WISHLIST = 'delete from tblWishList where fkUserId = ?'
DOES_BOOK_EXIST_WISHLIST = 'select pkWishListId from tblWishList where fkUserId = ? and fkBookId = ?'

class WishListRepository():
    def __init__(self):
        self.db =bookstoreContext.connection()
        self.cursor = self.db.cursor()

    def get_wishlist(self,fkUserId):
        return self.cursor.execute(SELECT_WISHLIST,(fkUserId,)).fetchall()

    def check_book_exists_wishlist(self, fkUserId,fkBookId):
        return self.cursor.execute(DOES_BOOK_EXIST_WISHLIST, (fkUserId, fkBookId,)).fetchone()

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

