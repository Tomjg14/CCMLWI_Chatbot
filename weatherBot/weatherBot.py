from database import dbhelper
from database import userDB

from handlers import textHandler
from handlers import inputHandler
from handlers import weatherHandler

from config import config

import json 
import requests
import urllib

from pyowm import OWM

class WeatherBot:

    def __init__(self):
        self.c = config.Config()
        self.mood = "neutral"
        self.th = textHandler.TextHandler()
        self.TOKEN = self.c.getToken()
        self.OWMKEY = self.c.getOWMKEY()
        self.URL = self.c.getURL()
        self.db = dbhelper.DBHelper()
        self.db.setup()
        self.user_db = userDB.UserDB()
        self.user_db.setup()
        self.wh = weatherHandler.WeatherHandler(self.OWMKEY)
        self.ih = inputHandler.InputHandler(self.mood,self.db,self.user_db,self.th,self.wh)

    '''
    Description: acquire messages sent to the bot
    :url: the url of the bot
    :content: the messages sent to the bot
    '''
    def get_content(self,url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    '''
    Description: Load the Jason from the bot URL
    :url: the url of the bot
    :js: The JSON object
    '''
    def get_json_from_url(self,url):
        content = self.get_content(url)
        js = json.loads(content)
        return js

    '''
    Description: acquire updates for the bot
    :offset: The format for the url
    :js: JSON object for the updates
    '''
    def get_updates(self,offset=None):
        url = self.URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    '''
    Description: Acquire the ID of the last update
    :updates: The list of updates
    :return: The highest update ID
    '''
    def get_last_update_id(self,updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    '''
    Description: Process the incoming updates using the user's mood
    :updates: The list of updates
    '''
    def handle_updates(self,updates):
        (message,chatid) = self.ih.handle_updates(updates,self.mood)
        self.send_message(message,chatid)

    '''
    Description: Acquire the last update ID + corresponding text
    :updates: The list of updates
    :text: The corresponding text
    :chat_id: The ID of the update of the corresponding text
    '''
    def get_last_chat_id_and_text(self,updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)

    '''
    Description: Send the response to the user
    :text: The text that should be sent
    :chat_id: The chatroom the message should be sent to
    :reply_markup: The format that should be added to the url
    '''
    def send_message(self,text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = self.URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        self.get_content(url)

    '''
    Description: Update the weather that determines the bot's mood
    '''
    def updateWeatherNimma(self):
        self.wh.setWeatherNimma()

    '''
    Description: Update the bot's mood based on the weather
    '''
    def updateMood(self):
        (weather,weather_code,temperature) = self.wh.getWeatherNimma()
        if weather_code == 800:
            self.mood = "happy"
        elif (801 <= weather_code <= 804) or (951 <= weather_code <= 955) or (weather_code == 701) or (600 <= weather_code <= 601):
            self.mood = "neutral"
        else:
            self.mood = "sad"

    def getMood(self):
        return self.mood
        
