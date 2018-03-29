import sqlite3
import os

class DBHelper:

    def __init__(self, dbname="database/weatherbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.txtfile = 'database/queries.txt'

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS items (sentiment text, tag text, text text)"
        sentimentidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (sentiment ASC)"
        tagidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (tag ASC)" 
        textidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (text ASC)"
        self.conn.execute(tblstmt)
        self.conn.execute(sentimentidx)
        self.conn.execute(tagidx)
        self.conn.execute(textidx)
        self.conn.commit()
        if self.dbEmpty():
            queries = self.readTXTFile()
            self.initializeDB(queries)

    def dbEmpty(self):
        empty = True
        items = self.get_items()
        #c = self.conn.cursor()
        #exist = c.fetchone()
        #print(exist)
        if len(items) > 0:
            empty = False
        print(empty)
        return empty

    def readTXTFile(self,):
        queries = []
        with open(self.txtfile) as infile:
            for line in infile:
                [sentiment,tag,text] = line.split("\t\t\t")
                queries.append((sentiment,tag,text.rstrip("\n")))
        return queries

    def initializeDB(self,queries):
        for (sentiment,tag, text) in queries:
            stmt = "INSERT INTO items (sentiment, tag, text) VALUES (?, ?, ?)"
            args = (sentiment, tag, text)
            self.conn.execute(stmt, args)
            self.conn.commit()

    def add_item(self, sentiment, tag, text):
        stmt = "INSERT INTO items (sentiment, tag, text) VALUES (?, ?, ?)"
        args = (sentiment, tag, text)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_text(self, sentiment, tag):
        stmt = "SELECT text FROM items WHERE sentiment = (?) AND tag = (?)"
        args = (sentiment, tag, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    def get_items(self):
        stmt = "SELECT * FROM items"
        return [x[0] for x in self.conn.execute(stmt)]

    def remove_item(self, sentiment, tag):
        stmt = "DELETE FROM items WHERE sentiment = (?) AND tag = (?)"
        args = (sentiment, tag, )
        self.conn.execute(stmt, args)
        self.conn.commit()

