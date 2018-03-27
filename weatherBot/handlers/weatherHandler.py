from pyowm import OWM

class WeatherHandler:

    def __init__(self,OWMKEY):
        self.owm = OWM(OWMKEY)

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

    
