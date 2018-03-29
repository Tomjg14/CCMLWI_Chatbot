import sqlite3
import os

'''
Class for handling the query database
'''
class DBHelper:

    def __init__(self, dbname="database/weatherbot.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.txtfile = 'database/queries.txt'

    '''
    Description: Sets up the database with the required indices
    '''
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

    '''
    Description: checks whether the database is empty or not
    :empty: true if empty, false if not
    '''
    def dbEmpty(self):
        empty = True
        items = self.get_items()
        if len(items) > 0:
            empty = False
        return empty

    '''
    Description: Reads the txt file containing the queries
    '''
    def readTXTFile(self):
        queries = []
        with open(self.txtfile) as infile:
            for line in infile:
                [sentiment,tag,text] = line.split("\t\t\t")
                queries.append((sentiment,tag,text.rstrip("\n")))
        return queries

    '''
    Description: Initializes the database with the queries from queries.txt
    :queries: queries from queries.txt
    '''
    def initializeDB(self,queries):
        for (sentiment,tag, text) in queries:
            stmt = "INSERT INTO items (sentiment, tag, text) VALUES (?, ?, ?)"
            args = (sentiment, tag, text)
            self.conn.execute(stmt, args)
            self.conn.commit()
    '''
    Description: Add an item to the database
    :sentiment: The sentiment of the text
    :tag: The type of text (e.g. greet)
    :text: The actual text
    '''
    def add_item(self, sentiment, tag, text):
        stmt = "INSERT INTO items (sentiment, tag, text) VALUES (?, ?, ?)"
        args = (sentiment, tag, text)
        self.conn.execute(stmt, args)
        self.conn.commit()

    '''
    Description: Acquire text from the database
    :sentiment: The sentiment of the text
    :tag: The tag of the text
    '''
    def get_text(self, sentiment, tag):
        stmt = "SELECT text FROM items WHERE sentiment = (?) AND tag = (?)"
        args = (sentiment, tag, )
        return [x[0] for x in self.conn.execute(stmt, args)]

    '''
    Description: Checks all elements that are in the database
    :return: the entire first column of the database
    '''
    def get_items(self):
        stmt = "SELECT * FROM items"
        return [x[0] for x in self.conn.execute(stmt)]

    '''
    Description: Removes a specific item from the database
    :sentiment: The sentiment of the item 
    :tag: The tag of the item
    '''
    def remove_item(self, sentiment, tag):
        stmt = "DELETE FROM items WHERE sentiment = (?) AND tag = (?)"
        args = (sentiment, tag, )
        self.conn.execute(stmt, args)
        self.conn.commit()

