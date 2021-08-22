from datacontext import bookstoreContext

SELECT_ALL = 'select pkUserId, sFirstName, sLastName, sEmail, sPassword from tblUser'
INSERT_USER = 'insert into tblUser(sFirstName, sLastName, sEmail, sPassword) values (?,?,?,?)'
SELECT_USER = 'select pkUserId, sFirstName, sLastName, sEmail, sPassword from tblUser where pkUserId = ?'
UPDATE_USER = 'update tblUser set sFirstName = ?, sLastName = ?, sEmail = ?, sPassword = ?  where pkUserId = ?'
DELETE_USER = 'delete from tblUser where pkUserId = ?'


class UserRepository():
    def __init__(self):
        self.db =bookstoreContext.connection()
        self.cursor = self.db.cursor()

    def get_all_users(self):
        return self.cursor.execute(SELECT_ALL).fetchall()

    def get_user(self,pkUserId):
        return self.cursor.execute(SELECT_USER,(pkUserId,)).fetchone()

    def add_user(self,user):
        self.cursor.execute(INSERT_USER,(user.sFirstName, user.sLastName, user.sEmail, user.sPassword, ))
        rowid = self.cursor.lastrowid
        self.db.commit()
        return rowid

    def delete_user(self, pkUserId):
        self.cursor.execute(DELETE_USER, (pkUserId,))
        self.db.commit()

    def update_user(self, pkUserId, user):
        self.cursor.execute(UPDATE_USER,(user.sFirstName, user.sLastName, user.sEmail, user.sPassword, pkUserId,))
        self.db.commit()
