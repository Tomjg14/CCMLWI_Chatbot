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

    '''
    Description: Process all the new updates
    :updates: A list containing the to be processed updates
    :mood: The current mood of the chatbot
    :message: The response of the chatbot for update
    :chatid: The ID of the chat the message was designed for
    '''
    def handle_updates(self,updates,mood):
        self.mood = mood
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
                (message,location) = self.location_update(update)
                self.store_input(chatid,messageid,"LOCATION",location,localtime)
                
            return (message,chatid)

    '''
    Description: Interpret and create a response for the incoming message
    :text: The incoming message
    :message: The response of the bot
    :location: The location of the weather report
    '''
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

    '''
    Description: Randomly picks a message that was inserted in the database
    :messages: All possible messages
    :message: The randomly picked message
    '''
    def pick_message(self,messages):
        if len(messages) > 1:
            message = random.choice(messages)
        else:
            message = messages[0]
        return message

    '''
    Description: Scans the text for placenames and generates a message
    :text: The text that is being scanned
    :message: The created message
    :location: The location that was extracted from the text
    '''
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
            

    '''
    Description: Create a message based on the observation for the correct location
    :update: The weather updates
    :message: The appropiate response based on the location
    '''
    def location_update(self,update):
        obs = self.wh.getWeatherFromLoc(update["message"]["location"])
        self.wh.set_weather_forecast(obs)
        location = self.wh.get_prev_loc()
        message = self.createWeatherMessage(location)
        return (message,location)

    '''
    Description: Pulls a message from the database based on mood and tag
    :tag: The tag of the message
    :message: The generated response
    '''
    def create_message(self,tag):
        message = self.db.get_text(self.mood,tag)
        print(message)
        return message

    '''
    Description: Store a message in the database
    :chatid: The ID of the chatroom the message originates from
    :messageid: The ID of the message that should be stored
    :text: The actual message
    :location: The location tag of the message
    :time: The time stamp of the message
    '''
    def store_input(self,chatid,messageid,text,location,time):
        self.user_db.add_item(chatid,messageid,text,location,time)

    '''
    Description: Creates a weather forecast message
    :location: The location of the forecast
    :message: The generated forecast message
    '''
    def createWeatherMessage(self,location):
        forecast = self.wh.get_weather_forecast(location)
        status = forecast["status"]
        placename = location
        wtime = forecast["wtime"]
        temperature = forecast["temperature"]
        message = "The weather at "+placename+" at "+wtime+" is: "+status+". The temperature is: "+temperature+"C."
        return message

    '''
    Description: Create a weather message for a specific weather type
    :location: The location for the weather message
    :info_type: The specific type of weather information
    :message: The generated message
    '''
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

        
