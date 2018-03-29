from pyowm import OWM
import time

class WeatherHandler:

    def __init__(self,OWMKEY):
        self.owm = OWM(OWMKEY)
        self.weather_dict = {}   #value voor in dictionary
        

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
        placename = str(l.getname())
        forecast["wtime"] = self.localtime
        forecast["status"] = str(w.get_detailed_status())
        forecast["temperature"] = str(w.get_temperature('celsius').get('temp'))

        self.weather_dict[placename] = forecast
        
