from pyowm import OWM
import time

class WeatherHandler:

    def __init__(self,OWMKEY):
        self.owm = OWM(OWMKEY)
        self.weather_dict = {}   #value voor in dictionary
        self.temp = ""
        self.weather = ""
        self.weather_code = 0

    def getWeatherFromLoc(self,location):
        obs = self.owm.weather_at_coords(location["latitude"],location["longitude"])
        return obs

    def getWeatherFromPlace(self,place):
        obs = self.owm.weather_at_place(place)
        return obs

    def getLocations(self,placename):
        reg = self.owm.city_id_registry()
        locations = reg.locations_for(placename)
        return locations

    def getWeatherFromID(self,location):
        city_id = location.get_ID()
        obs = self.owm.weather_at_id(city_id)
        return obs

    def get_specific_info(self,placename,infotype):
        return self.weather_dict[placename][infotype]

    def get_weather_forecast(self,placename):
        return self.weather_dict[placename]

    def set_weather_forecast(self,obs):
        forecast = {}
        w = obs.get_weather()
        l = obs.get_location()
        placename = str(l.get_name())
        forecast["wtime"] = time.asctime(time.localtime(time.time()))
        forecast["status"] = str(w.get_detailed_status())
        forecast["temperature"] = str(w.get_temperature('celsius').get('temp'))
        forecast["code"] = w.get_weather_code()

        self.weather_dict[placename] = forecast

    def setWeatherNimma(self):
        obs = self.owm.weather_at_place("Nijmegen,NL")
        w = obs.get_weather()
        self.weather = str(w.get_detailed_status())
        self.temp = str(w.get_temperature('celsius').get('temp'))
        self.weather_code = w.get_weather_code()

    def getWeatherNimma(self):
        return (self.weather,self.weather_code,self.temp)
