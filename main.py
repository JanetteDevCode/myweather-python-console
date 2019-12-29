from dotenv import load_dotenv


load_dotenv()


import sys, geocode_console, weather_console
from geocode_api_request import GeocodeApiRequest
from weather_api_request import WeatherApiRequest
from geocode import Geocode
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

def process_weather_choice(weather, choice=''):
    results = {}
    choice = choice.strip()

    print()

    if choice == 'Q':
        print("Goodbye.")
        return False
    elif choice == weather_choices['currently']['id']:
        results = weather.get_current_weather()
        if results['status'] == 'OK':
            weather_console.display_alerts_count(results['alerts'])
            weather_console.display_currently(
                results['location'], results['timezone'], results['currently'])
        # print(weather_choices['currently']['description'])
    elif choice == weather_choices['hourly']['id']:
        results = weather.get_hourly_weather()
        if results['status'] == 'OK':
            weather_console.display_alerts_count(results['alerts'])
            weather_console.display_hourly(
                results['location'], results['timezone'], results['hourly'])
        # print(weather_choices['hourly']['description'])
    elif choice == weather_choices['today']['id']:
        results = weather.get_today_weather()
        if results['status'] == 'OK':
            weather_console.display_alerts_count(results['alerts'])
            weather_console.display_today(
                results['location'], results['timezone'], results['today'])
        # print(weather_choices['today']['description'])
    elif choice == weather_choices['daily']['id']:
        results = weather.get_daily_weather()
        if results['status'] == 'OK':
            weather_console.display_alerts_count(results['alerts'])
            weather_console.display_daily(
                results['location'], results['timezone'], results['daily'])
        # print(weather_choices['daily']['description'])
    elif choice == weather_choices['alerts']['id']:
        results = weather.get_weather_alerts()
        if results['status'] == 'OK':
            weather_console.display_alerts(
                results['location'], results['timezone'], results['alerts'])
        # print(weather_choices['alerts']['description'])
    else:
        results = {'status': 'ERROR', 'error': "Invalid selection."}

    if results['status'] == 'ERROR':
        print(results['error'])

    print()

    return True

def get_user_address():
    return input("Enter address: ")

def get_geocode(address):
    results = {
        'status': '',
        'error': '',
        'location': '',
        'latitude': 0,
        'longitude': 0
    }
    geocode_json = GeocodeApiRequest.get_geocode_json(address)

    if geocode_json['info']['statuscode'] != 0:
        results['status'] = 'ERROR'
        results['error'] = ("Error! Could not retrieve geocode data.")
    else:
        usa_locations = list(filter(
                lambda location: location['adminArea1'] == "US", 
                geocode_json['results'][0]['locations']
            )
        )
        # print(usa_locations)
        city = usa_locations[0]['adminArea5']
        state = usa_locations[0]['adminArea3']
        results['status'] = 'OK'
        results['location'] = ("{city}, {state}".format(city=city, state=state))
        results['latitude'] = usa_locations[0]['latLng']['lat']
        results['longitude'] = usa_locations[0]['latLng']['lng']

    return results

def api_keys_exist():
    if not (GeocodeApiRequest.api_key or WeatherApiRequest.api_key):
        print("Missing API keys for geocoding and weather APIs!")
        print("Obtain the keys and store them as environment variables")
        print("named MAPQUEST_OPEN_GEOCODING_API_KEY and DARKSKY_API_KEY.")
        return False
    elif not GeocodeApiRequest.api_key:
        print("Missing API key for geocoding API!")
        print("Obtain the key and store it as an environment variable")
        print("named MAPQUEST_OPEN_GEOCODING_API_KEY.")
        return False
    elif not WeatherApiRequest.api_key:
        print('Missing API key for weather API!')
        print("Obtain the key and store it as an environment variable")
        print("named DARKSKY_API_KEY.")
        return False
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
print("Geolocation powered by: MapQuest Open Geocoding")
print("  [https://developer.mapquest.com/documentation/open/geocoding-api/]")
print()

if not api_keys_exist():
    sys.exit()

locations_result = Geocode.get_locations(get_user_address())

if locations_result['status'] == 'OK':
    selected_location = geocode_console.get_user_location_choice(locations_result['locations'])

    print()
    print("Location: {0}".format(selected_location['location']))
    print("Latitude: {0}, Longitude: {1}".format(selected_location['latitude'], selected_location['longitude']))
    print()

    weather = Weather(selected_location['location'], selected_location['latitude'], selected_location['longitude'])

    while True:
        display_weather_choice_menu()
        choice = input("Enter weather report choice: ")
        if not process_weather_choice(weather, choice):
            break
        else:
            input("--- Press 'Enter' to continue. --- ")
            print()
else:
    print(locations_result['error'])


# if geocode['status'] == 'OK':
#     print()
#     print("Location: {0}".format(geocode['location']))
#     print("Latitude: {0}, Longitude: {1}".format(geocode['latitude'], geocode['longitude']))
#     print()

#     weather = Weather(geocode['location'], geocode['latitude'], geocode['longitude'])

#     while True:
#         display_weather_choice_menu()
#         choice = input("Enter weather report choice: ")
#         if not process_weather_choice(weather, choice):
#             break
#         else:
#             input("--- Press 'Enter' to continue. --- ")
#             print()
# else:
#     print(geocode['error'])
