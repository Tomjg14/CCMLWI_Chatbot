import sqlite3


class UserDB:
    def __init__(self, dbname="database/chat_history.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        print("creating table")
        stmt = "CREATE TABLE IF NOT EXISTS items (owner text, messageid int, chat text, location text, time text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, owner, messageid, chat, location, time):
        stmt = "INSERT INTO items (owner, messageid, chat, location, time) VALUES (?, ?, ?, ?, ?)"
        args = (owner, messageid, chat, location, time)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, owner, messageid):
        stmt = "DELETE FROM items WHERE owner = (?) AND messageid = (?)"
        args = (owner, messageid)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_item(self, owner, messageid):
        stmt = "SELECT chat FROM items WHERE owner = (?) AND messageid = (?)"
        args = (owner, messageid)
        return [x[0] for x in self.conn.execute(stmt, args)]
