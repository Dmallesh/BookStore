from datacontext import bookstoreContext

SELECT_ALL = 'select pkBookId, sTitle, sAuthor, sISBN, dtPublished from tblBook'
INSERT_BOOK = 'insert into tblBook(sTitle, sAuthor, sISBN, dtPublished) values (?,?,?,?)'
SELECT_BOOK = 'select pkBookId, sTitle, sAuthor, sISBN, dtPublished from tblBook where pkBookId = ?'
UPDATE_BOOK = 'update tblBook set sTitle = ?, sAuthor = ?, sISBN = ?, dtPublished = ?  where pkBookId = ?'
DELETE_BOOK = 'delete from tblBook where pkBookId = ?'


class BookRepository():
    def __init__(self):
        self.db =bookstoreContext.connection()
        self.cursor = self.db.cursor()

    def get_all_books(self):
        return self.cursor.execute(SELECT_ALL).fetchall()

    def get_book(self,pkBookId):
        return self.cursor.execute(SELECT_BOOK,(pkBookId,)).fetchone()

    def add_book(self,book):
        self.cursor.execute(INSERT_BOOK,(book.sTitle, book.sAuthor, book.sISBN, book.dtPublished, ))
        rowid = self.cursor.lastrowid
        self.db.commit()
        return rowid

    def delete_book(self, pkBookId):
        self.cursor.execute(DELETE_BOOK, (pkBookId,))
        self.db.commit()

    def update_book(self, pkBookId, book):
        self.cursor.execute(UPDATE_BOOK,(book.sTitle, book.sAuthor, book.sISBN, book.dtPublished, pkBookId,))
        self.db.commit()
