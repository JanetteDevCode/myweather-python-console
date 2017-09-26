import sys
from geocode_api_request import GeocodeApiRequest
from weather_api_request import WeatherApiRequest
from weather import Weather

#    __  __        __          __        _   _
#   |  \/  |       \ \        / /       | | | |
#   | \  / |_   _   \ \  /\  / /__  __ _| |_| |__   ___ _ __
#   | |\/| | | | |   \ \/  \/ / _ \/ _` | __| '_ \ / _ \ '__|
#   | |  | | |_| |    \  /\  /  __/ (_| | |_| | | |  __/ |
#   |_|  |_|\__, |     \/  \/ \___|\__,_|\__|_| |_|\___|_|
#            __/ |
#           |___/
print("+-----------------------------------------------------------------+")
print("|     __  __        __          __        _   _                   |")
print("|    |  \/  |       \ \        / /       | | | |                  |")
print("|    | \  / |_   _   \ \  /\  / /__  __ _| |_| |__   ___ _ __     |")
print("|    | |\/| | | | |   \ \/  \/ / _ \/ _` | __| '_ \ / _ \ '__|    |")
print("|    | |  | | |_| |    \  /\  /  __/ (_| | |_| | | |  __/ |       |")
print("|    |_|  |_|\__, |     \/  \/ \___|\__,_|\__|_| |_|\___|_|       |")
print("|             __/ |                                               |")
print("|            |___/                                                |")
print("+-----------------------------------------------------------------+")
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
# weather.get_current_weather()
# weather.get_hourly_weather()
# weather.get_daily_weather()
weather.get_today_weather()
