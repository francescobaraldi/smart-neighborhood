import requests
import json
import urllib.parse


class OpenWeather:
    def __init__(self, address, api_key):
        self.address = address # 'Carpi, Italia'
        self.api_key = api_key
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json'
        response = requests.get(url).json()[0]
        self.lat = response["lat"]
        self.lon = response["lon"]
        self.url = "https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s" % (self.lat, self.lon, self.api_key)
    
    def get_data(self):
        response = requests.get(self.url)
        data = json.loads(response.content)
        # temp = self.data['main']['temp'] - 273.15
        return data
