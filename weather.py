import json, requests


class ApiRequest:
    @classmethod
    def make_api_request(cls, uri='', params={}, timeout=10):
        try:
            req = requests.get(uri, params=params, timeout=timeout)
            return req.json()
        except Exception as e:
            return {'error': e}


class Weather:
    def __init__(self, latitude=37.8267, longitude=-122.4233):
        self.latitude = latitude
        self.longitude = longitude

    def get_darksky_uri(self):
        return ('https://api.darksky.net/forecast/'
            + '7f560844e81c036d5e8beafb449eda24' + '/'
            + str(self.latitude) + ',' + str(self.longitude))

    def get_current_weather(self):
        exclude = 'minutely,hourly,daily,flags'
        return ApiRequest.make_api_request(self.get_darksky_uri(),
            {'exclude': exclude})


myweather = Weather()
current_weather = myweather.get_current_weather()
if 'error' in current_weather:
    print("Oops. An error has occurred.")
    print(str(current_weather['error']))
else:
    for k, v in current_weather['currently'].items():
        print("{0}: {1}".format(k, v))
