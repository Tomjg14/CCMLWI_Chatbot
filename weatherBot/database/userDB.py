import sqlite3

'''
Class for handling the chat history database
'''
class UserDB:
    def __init__(self, dbname="database/chat_history.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    '''
    Description: sets up the database with the required indices
    '''
    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (owner text, messageid int, chat text, location text, time text)"
        self.conn.execute(stmt)
        self.conn.commit()

    '''
    Description: Adds a new item to the database
    :owner: The ID of the owner of the chat message
    :messageid: The ID of the chat message
    :chat: The text of the chat message
    :location: The location the chat message was sent from
    :time: The time stamp of the chat message
    '''
    def add_item(self, owner, messageid, chat, location, time):
        stmt = "INSERT INTO items (owner, messageid, chat, location, time) VALUES (?, ?, ?, ?, ?)"
        args = (owner, messageid, chat, location, time)
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    '''
    Description: Deletes a specific element from the database
    :owner: The ID of the owner of the item
    :messageid: The messageID of the item
    '''
    def delete_item(self, owner, messageid):
        stmt = "DELETE FROM items WHERE owner = (?) AND messageid = (?)"
        args = (owner, messageid)
        self.conn.execute(stmt, args)
        self.conn.commit()

    '''
    Description: Acquire a specific item from the database
    :owner: The ID of the owner of the item
    :messageid: The messageID of the item
    :return: The requested item
    '''
    def get_item(self, owner, messageid):
        stmt = "SELECT chat FROM items WHERE owner = (?) AND messageid = (?)"
        args = (owner, messageid)
        return [x[0] for x in self.conn.execute(stmt, args)]
