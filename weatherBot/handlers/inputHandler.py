import time
import random

class InputHandler:

    def __init__(self,mood,db,user_db,th,wh):
        self.mood = mood
        self.db = db
        self.user_db = user_db
        self.th = th
        self.wh = wh
        self.localtime = time.asctime(time.localtime(time.time()))

    def handle_updates(self,updates):
        localtime = time.asctime(time.localtime(time.time()))
        for update in updates["result"]:
            chatid = update["message"]["chat"]["id"]
            messageid = update["message"]["message_id"]
            attributes = update["message"].keys()
            if "text" in attributes:
                text = update["message"]["text"]
                (message,location) = self.text_update(text)
                self.store_input(chatid,messageid,text,location,localtime)
            elif "location" in attributes:
                (message,location) = self.location_update(update,chatid)
                self.store_input(chatid,messageid,"LOCATION",location,localtime)
                
            return (message,chatid)

    def text_update(self,text):
        location = ""
        if self.th.is_hi(text):
            messages = self.create_message("greet")
            message = self.pick_message(messages)
        elif self.th.mood(text):
            messages = self.create_message("mood")
            message = self.pick_message(messages)
        elif self.th.need_help(text):
            messages = self.create_message("help")
            message = self.pick_message(messages)
        elif self.th.is_bye(text):
            messages = self.create_message("bye")
            message = self.pick_message(messages)
        elif self.th.need_temp(text):
            location = self.wh.get_prev_loc()
            message = self.createSpecificWeatherMessage(location,"temperature")
        elif self.th.need_status(text):
            location = self.wh.get_prev_loc()
            message = self.createSpecificWeatherMessage(location,"status")
        elif self.th.need_forecast(text):
            location = self.wh.get_prev_loc()
            message = self.createWeatherMessage(location)
        else:
            (message,location) = self.check_for_places(text)
        return (message,location)

    def pick_message(self,messages):
        if len(messages) > 1:
            message = random.choice(messages)
        else:
            message = messages[0]
        return message

    def check_for_places(self,text):
        location = ""
        places = self.th.get_chunks(text,"GPE")
        if len(places) > 0:
            location = places[0]
            obs = self.wh.getWeatherFromPlace(location)
            self.wh.set_weather_forecast(obs)
            message = self.create_message("location")[0]
            message = "%s %s? Would you like the temperature, weather status or the entire forecast?"%(message,location)
        else:
            places = []
            tokens = self.th.tokenize_text(text)
            tagged = self.th.compute_pos(tokens)
            nnp_list = self.th.get_NNP(tagged)
            nn_list = self.th.get_NN(tagged)
            for nnp in nnp_list:
                places = places + self.wh.getLocations(nnp)
            for nn in nn_list:
                places = places + self.wh.getLocations(nn)
            if len(places) > 0:
                obs = self.wh.getWeatherFromID(places[0])
                l = obs.get_location()
                location = str(l.get_name())
                self.wh.set_weather_forecast(obs)
                message = self.create_message("location")[0]
                message = "%s %s? Would you like the temperature, weather status or the entire forecast?"%(message,location)
            else:
                message = self.create_message("unclear")[0]
        return (message,location)
            

    def location_update(self,update,chatid):
        obs = self.wh.getWeatherFromLoc(update["message"]["location"])
        (message,location) = self.createWeatherMessage(obs)
        return message

    def create_message(self,tag):
        message = self.db.get_text(self.mood,tag)
        print(message)
        return message

    def store_input(self,chatid,messageid,text,location,time):
        self.user_db.add_item(chatid,messageid,text,location,time)

    def createWeatherMessage(self,location):
        forecast = self.wh.get_weather_forecast(location)
        status = forecast["status"]
        placename = location
        wtime = forecast["wtime"]
        temperature = forecast["temperature"]
        message = "The weather at "+placename+" at "+wtime+" is: "+status+". The temperature is: "+temperature+"C."
        return message

    def createSpecificWeatherMessage(self,location,info_type):
        if info_type == "temperature":
            temperature = self.wh.get_specific_info(location,info_type)
            message = "The temperature at "+location+" is: "+temperature+"C."
            return message
        elif info_type == "status":
            location = "Nijmegen"
            status = self.wh.get_specific_info(location,info_type)
            message = "The current weather status at "+location+" is: "+status+"."
            return message
        else:
            return "I do not understand this request. Please try again"

        
