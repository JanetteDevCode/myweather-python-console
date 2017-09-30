import sys
from geocode_api_request import GeocodeApiRequest
from weather_api_request import WeatherApiRequest
from weather import Weather

weather_choices = {
    'currently': {'id': 'C', 'description': "Current conditions"},
    'hourly': {'id': 'H', 'description': "Hourly forecast"},
    'today': {'id': 'T', 'description': "Today's forecast"},
    'daily': {'id': 'D', 'description': "Daily forecast"},
    'alerts': {'id': 'A', 'description': "Alerts"},
}

def display_weather_choice_menu():
    print("===================")
    print("Weather Report Menu")
    print("===================")
    print()
    for choice in weather_choices:
        print("'{0}' - {1}".format(
            weather_choices[choice]['id'],
            weather_choices[choice]['description']))
    print("'Q' - Quit")
    print()

def process_weather_choice(choice=''):
    choice = choice.strip()
    print()
    if choice == 'Q':
        print("Goodbye.")
        return False
    elif choice == weather_choices['currently']['id']:
        weather.get_current_weather()
        # print(weather_choices['currently']['description'])
    elif choice == weather_choices['hourly']['id']:
        weather.get_hourly_weather()
        # print(weather_choices['hourly']['description'])
    elif choice == weather_choices['today']['id']:
        weather.get_today_weather()
        # print(weather_choices['today']['description'])
    elif choice == weather_choices['daily']['id']:
        weather.get_daily_weather()
        # print(weather_choices['daily']['description'])
    elif choice == weather_choices['alerts']['id']:
        weather.get_weather_alerts()
        # print(weather_choices['alerts']['description'])
    else:
        print("Invalid selection.")
    print()
    return True

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
print("Copyright 2017 Janette H. Griggs")
print()
print("Weather data powered by: Dark Sky")
print("  [https://darksky.net/poweredby/]")
print()
print("Geolocation powered by: Google Maps Geocoding")
print("  [https://developers.google.com/maps/documentation/geocoding/start]")
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
    print()

weather = Weather(zip_code, latitude, longitude)

while True:
    display_weather_choice_menu()
    choice = input("Enter weather report choice: ")
    if not process_weather_choice(choice):
        break
    else:
        input("--- Press 'Enter' to continue. --- ")
        print()
