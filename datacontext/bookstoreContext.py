import sqlite3

def connection():
        return sqlite3.connect(r'BookStore.db', check_same_thread=False)


