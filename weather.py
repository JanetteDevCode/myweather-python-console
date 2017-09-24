import json, re, requests, sys


class ApiRequest:
    @classmethod
    def make_api_request(cls, uri='', params={}, timeout=10):
        try:
            req = requests.get(uri, params=params, timeout=timeout)
            # print(req.url)
            return req.json()
        except Exception as e:
            return {'error': e}


class Geocode:
    googlemapsgeocoding_api_key = 'AIzaSyBO5h570rjeDP9Cz8KkCeAFwX-NHu0fLkQ'

    @classmethod
    def get_googlemapsgeocoding_uri(cls):
        return ('https://maps.googleapis.com/maps/api/geocode/json')

    @classmethod
    def get_geocode_json(cls, zip_code):
        return ApiRequest.make_api_request(cls.get_googlemapsgeocoding_uri(),
            {'components': 'postal_code:' + zip_code,
            'key': Geocode.googlemapsgeocoding_api_key})


class Weather:
    darksky_api_key = '7f560844e81c036d5e8beafb449eda24'

    def __init__(self, latitude=37.8267, longitude=-122.4233):
        self.latitude = latitude
        self.longitude = longitude

    def get_darksky_uri(self):
        return ('https://api.darksky.net/forecast/'
            + Weather.darksky_api_key + '/'
            + str(self.latitude) + ',' + str(self.longitude))

    def get_current_weather_json(self):
        exclude = 'minutely,hourly,daily,flags'
        return ApiRequest.make_api_request(self.get_darksky_uri(),
            {'exclude': exclude})


print("-----------------------------")
print("---- My Weather Forecast ----")
print("-----------------------------")
print()

zip_code = input("Enter ZIP code: ")
geocode_json = Geocode.get_geocode_json(zip_code)

if geocode_json['status'] != 'OK' or 'error' in geocode_json:
    print("Error! Could not retrieve geocode data.")
    sys.exit()
else:
    latitude = geocode_json['results'][0]['geometry']['location']['lat']
    longitude = geocode_json['results'][0]['geometry']['location']['lng']
    print()
    print("ZIP Code: {0}".format(zip_code))
    print("Latitude: {0}, Longitude: {1}".format(latitude, longitude))

weather = Weather(latitude, longitude)
current_weather_json = weather.get_current_weather_json()

print()
print("Current Weather for {0}".format(zip_code))
print("--------------------{0}".format('-' * len(zip_code)))
print()

if 'error' in current_weather_json:
    print("Error! Could not retrieve current weather data.")
else:
    for k, v in current_weather_json['currently'].items():
        label = k.replace(k[0], k[0].upper(), 1)
        label = re.findall('[A-Z][^A-Z]*', label)
        label = ' '.join(label) + ':'
        value = v
        print("{0:<30} {1:>15} ({2})".format(label, value, type(value)))
