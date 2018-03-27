import time

class InputHandler:

    def __init__(self,db,user_db,th,wh):
        self.db = db
        self.user_db = user_db
        self.th = th
        self.wh = wh
        tags = db.get_tags()
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

    '''
    This function needs improvement!!
    at the moment it only checks for 3 basic input types.
    Should be more dynamic, so that it reacts on words like hi, hello, how are you etc... as well.
    '''
    def text_update(self,text):
        print(text)
        location = ""
        if text == "hello":
            message = self.create_message("greet")[0]
        elif text == "help":
            message = self.create_message("help")[0]
        elif text == "bye":
            message = self.create_message("bye")[0]
        else:
            places = self.th.get_chunks(text,"GPE")
            if len(places) > 0:
                location = places[0]
                obs = self.wh.getWeatherFromPlace(location)
                (message,location) = self.createWeatherMessage(obs)
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
                    (message,location) = self.createWeatherMessage(obs)
                else:
                    message = self.create_message("help")
        return (message,location)

    def location_update(self,update,chatid):
        obs = self.wh.getWeatherFromLoc(update["message"]["location"])
        (message,location) = self.createWeatherMessage(obs)
        return message

    def create_message(self,tag):
        message = self.db.get_text(tag)
        return message

    def store_input(self,chatid,messageid,text,location,time):
        self.user_db.add_item(chatid,messageid,text,location,time)

    '''
    weather message is very static
    instead it would be better if the weatherbot stores the individual parts
    and only returns the parts that were asked for
    example: "How warm is it in Nijmegen? A: it is ... Celsius"
    example: "What is the weather like in Nijmegen? A: it is cloudy. Could you maybe tell me how warm it is as well? A: it is ... Celsius"
    '''
    def createWeatherMessage(self,obs):
        w = obs.get_weather()
        l = obs.get_location()
        status = str(w.get_detailed_status())
        placename = str(l.get_name())
        #wtime = str(w.get_reference_time(timeformat='iso'))
        wtime = self.localtime
        temperature = str(w.get_temperature('celsius').get('temp'))
        message = "Weather Status: "+status +" At "+placename+" "+wtime+" Temperature: "+ temperature+"C"
        return (message,placename)

        
