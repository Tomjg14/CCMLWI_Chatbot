from pyowm import OWM
import time

class WeatherHandler:

    def __init__(self,OWMKEY):
        self.owm = OWM(OWMKEY)
        self.weather_dict = {}   #value voor in dictionary
        self.temp = ""
        self.weather = ""
        self.weather_code = 0
        self.prev_loc = ""

    '''
    Description: Get weather observation from location coordinates
    :location: the location for the observation
    :obs: The weather observation
    '''
    def getWeatherFromLoc(self,location):
        obs = self.owm.weather_at_coords(location["latitude"],location["longitude"])
        return obs

    '''
    Description: Get weather observation from a named place
    :place: the placename for the observation
    :obs: The weather observation
    '''
    def getWeatherFromPlace(self,place):
        obs = self.owm.weather_at_place(place)
        return obs

    '''
    Description: Get possible locations belonging to a placename
    :placename: the placename for the location list
    :obs: The possible locations
    '''
    def getLocations(self,placename):
        reg = self.owm.city_id_registry()
        locations = reg.locations_for(placename)
        return locations

    '''
    Description: Get weather observation from a location ID
    :place: the location ID
    :obs: The weather observation
    '''
    def getWeatherFromID(self,location):
        city_id = location.get_ID()
        obs = self.owm.weather_at_id(city_id)
        return obs

    '''
    Description: Get specific weather info for a location
    :placename: the placename for the weather info
    :weatherinfo: the type of weather info
    :return: The desired information
    '''
    def get_specific_info(self,placename,infotype):
        return self.weather_dict[placename][infotype]

    '''
    Description: Get an entire forecast for a place
    :place: the placename for the forecast
    :return: the forecast
    '''
    def get_weather_forecast(self,placename):
        return self.weather_dict[placename]

    '''
    Description: Add a new entry to the dictionary of weather forecasts
    :obs: the weather observation that should be added
    '''
    def set_weather_forecast(self,obs):
        forecast = {}
        w = obs.get_weather()
        l = obs.get_location()
        placename = str(l.get_name())
        self.prev_loc = placename
        forecast["wtime"] = time.asctime(time.localtime(time.time()))
        forecast["status"] = str(w.get_detailed_status())
        forecast["temperature"] = str(w.get_temperature('celsius').get('temp'))
        forecast["code"] = w.get_weather_code()
        self.weather_dict[placename] = forecast

    '''
    Description: Set the weather for the hometown of the bot (Nijmegen)
    '''
    def setWeatherNimma(self):
        obs = self.owm.weather_at_place("Nijmegen,NL")
        w = obs.get_weather()
        self.weather = str(w.get_detailed_status())
        self.temp = str(w.get_temperature('celsius').get('temp'))
        self.weather_code = w.get_weather_code()

    '''
    Description: Get weather information for Nijmegen
    :return: Weather information for Nijmegen
    '''
    def getWeatherNimma(self):
        return (self.weather,self.weather_code,self.temp)

    '''
    Description: Acquire the previous location
    :return: the previous location
    '''
    def get_prev_loc(self):
        return self.prev_loc
