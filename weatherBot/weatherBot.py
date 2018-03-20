from dbhelper import DBHelper

import json 
import requests
import urllib
from config import Config

from pyowm import OWM

class WeatherBot:

    def __init__(self):
        self.c = Config()
        self.TOKEN = self.c.getToken()
        self.OWMKEY = self.c.getOWMKEY()
        self.URL = self.c.getURL()
        self.db = DBHelper()
        self.owm = OWM(self.OWMKEY)

    def initializeDB(self):
        self.db.setup()

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
        for update in updates["result"]:
            chatid = update["message"]["chat"]["id"]
            attributes = update["message"].keys()
            if "text" in attributes:
                text = update["message"]["text"]
                items = self.db.get_items(chatid)  ##
                if text == "/start":
                    self.send_message("Hi there! I am your personal Weather Bot, here to help you answer questions related to the weather. Just send me a location or placename to get started.", chatid)
                elif text.startswith("/"):
                    continue
                else:
                    locations = self.getLocations(text)
                    obs = self.getWeatherFromPlace(text)
                    weather_message = self.createWeatherMessage(obs)
                    self.send_message(weather_message,chatid)
            elif "location" in attributes:
                obs = self.getWeatherFromLoc(update["message"]["location"])
                weather_message = self.createWeatherMessage(obs)
                self.send_message(weather_message,chatid)
                

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

    def getWeatherFromPlace(self,place):
        obs = self.owm.weather_at_place(place)
        return obs

    def getLocations(self,placename):
        reg = self.owm.city_id_registry()
        locations = reg.locations_for(placename)
        return locations
        
    def getWeatherFromLoc(self,location):
        obs = self.owm.weather_at_coords(location["latitude"],location["longitude"])
        return obs

    def createWeatherMessage(self,obs):
        w = obs.get_weather()
        l = obs.get_location()
        status = str(w.get_detailed_status())
        placename = str(l.get_name())
        wtime = str(w.get_reference_time(timeformat='iso'))
        temperature = str(w.get_temperature('celsius').get('temp'))
        message = "Weather Status: "+status +" At "+placename+" "+wtime+" Temperature: "+ temperature+"C"
        return message
        
