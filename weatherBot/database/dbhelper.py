import sqlite3

class DBHelper:

    def __init__(self, dbname="database/weatherbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.txtfile = 'database/queries.txt'

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (tag text, text text)"
        tagidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (tag ASC)" 
        textidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (text ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(tagidx)
        self.conn.execute(textidx)
        self.conn.commit()
        queries = self.readTXTFile()
        self.initializeDB(queries)

    def readTXTFile(self,):
        queries = {}
        with open(self.txtfile) as infile:
            for line in infile:
                [tag,text] = line.split("\t\t\t")
                queries[tag] = text.rstrip("\n")
        return queries

    def initializeDB(self,queries):
        for tag, text in queries.items():
            stmt = "INSERT INTO items (tag, text) VALUES (?, ?)"
            args = (tag, text)
            self.conn.execute(stmt, args)
            self.conn.commit()

    def add_item(self, tag, text):
        stmt = "INSERT INTO items (tag, text) VALUES (?, ?)"
        args = (tag, text)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_text(self, tag):
        stmt = "SELECT text FROM items WHERE tag = (?)"
        args = (tag, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_tags(self):
        stmt = "SELECT tag FROM items"
        args = ()
        return [x[0] for x in self.conn.execute(stmt, args)]

    def remove_item(self, tag):
        stmt = "DELETE FROM items WHERE tag = (?)"
        args = (tag,)
        self.conn.execute(stmt, args)
        self.conn.commit()

