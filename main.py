import sys
from geocode_api_request import GeocodeApiRequest
from weather_api_request import WeatherApiRequest
from weather import Weather


print("-----------------------------")
print("---- My Weather Forecast ----")
print("-----------------------------")
print()

zip_code = input("Enter ZIP code: ")
geocode_json = GeocodeApiRequest.get_geocode_json(zip_code)

if geocode_json['status'] != 'OK' or 'error' in geocode_json:
    print("Error! Could not retrieve geocode data.")
    sys.exit()
else:
    latitude = geocode_json['results'][0]['geometry']['location']['lat']
    longitude = geocode_json['results'][0]['geometry']['location']['lng']
    print()
    print("ZIP Code: {0}".format(zip_code))
    print("Latitude: {0}, Longitude: {1}".format(latitude, longitude))

weather = Weather(zip_code, latitude, longitude)
weather.get_current_weather()
