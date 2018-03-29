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
        
    def get_content(self,url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content

    def get_json_from_url(self,url):
        content = self.get_content(url)
        js = json.loads(content)
        return js

    def get_updates(self,offset=None):
        url = self.URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js

    def get_last_update_id(self,updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def handle_updates(self,updates):
        (message,chatid) = self.ih.handle_updates(updates)
        self.send_message(message,chatid)

    def get_last_chat_id_and_text(self,updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)

    def send_message(self,text, chat_id, reply_markup=None):
        text = urllib.parse.quote_plus(text)
        url = self.URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        if reply_markup:
            url += "&reply_markup={}".format(reply_markup)
        self.get_content(url)

    def build_keyboard(self,items):
        keyboard = [[item] for item in items]
        reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def updateWeatherNimma(self):
        self.wh.setWeatherNimma()

    def updateMood(self):
        (weather,weather_code,temperature) = self.wh.getWeatherNimma()
        if weather_code == 800:
            self.mood = "happy"
        elif (801 >= weather_code <= 804) or (951 >= weather_code <= 955) or (weather_code == 701) or (600 >= weather_code <= 601):
            self.mood = "sad"
        else:
            self.mood = "sad"
        
