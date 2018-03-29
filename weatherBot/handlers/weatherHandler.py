from pyowm import OWM

class WeatherHandler:

    def __init__(self,OWMKEY):
        self.owm = OWM(OWMKEY)
        self.temp = ""
        self.weather = ""

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

    def setWeatherNimma(self):
        obs = self.owm.weather_at_place("Nijmegen,NL")
        w = obs.get_weather()
        self.weather = str(w.get_detailed_status())
        self.temp = str(w.get_temperature('celsius').get('temp'))

    def getWeatherNimma(self):
        return (self.weather,self.temp)

    
