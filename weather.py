import re
from datetime import datetime
from pytz import timezone
from weather_api_request import WeatherApiRequest


class Weather:
    def __init__(self, zip_code, latitude, longitude):
        self.__zip_code = zip_code
        self.__latitude = latitude
        self.__longitude = longitude

    def get_current_weather(self):
        weather_json = WeatherApiRequest.get_current_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            print("Error! Could not retrieve current weather data.")
        else:
            weather_timezone = timezone(weather_json['timezone'])

            print()
            print("Current Weather for {0}".format(self.__zip_code))
            print("--------------------{0}".format('-' * len(self.__zip_code)))
            print()
            print("Latitude: {0}, Longitude: {1}".format(
                    weather_json['latitude'],
                    weather_json['longitude'])
                )
            print("Timezone:", weather_timezone.zone)

            if 'alerts' in weather_json:
                for i, v in enumerate(weather_json['alerts'], start=1):
                    print('*' * 80)
                    print("Alert #{0}".format(i))
                    print(v['severity'].upper(), end=': ')
                    print(v['title'])
                    alert_time = weather_timezone.localize(datetime.fromtimestamp(v['time']))
                    print("Issued at: {:%Y-%m-%d %I:%M:%S %p %Z}".format(alert_time))
                    alert_expires = weather_timezone.localize(datetime.fromtimestamp(v['expires']))
                    print("Expires at: {:%Y-%m-%d %I:%M:%S %p %Z}".format(alert_expires))
                    print("Regions affected:", end=' ')
                    alert_regions = v['regions']
                    alert_regions_count = len(alert_regions)
                    for i, r in enumerate(alert_regions, start=1):
                        if i == alert_regions_count:
                            print(r)
                        else:
                            print(r, end=', ')
                    print("Description:")
                    print(v['description'], end='')
                print('*' * 80)

            if 'currently' in weather_json:
                for k, v in weather_json['currently'].items():
                    label = k.replace(k[0], k[0].upper(), 1)
                    label = re.findall('[A-Z][^A-Z]*', label)
                    label = ' '.join(label) + ':'
                    if k == 'time':
                        currently_time = weather_timezone.localize(datetime.fromtimestamp(v))
                        print("Date: {:%Y-%m-%d}".format(currently_time))
                        print("Time: {:%I:%M:%S %p %Z}".format(currently_time))
                    else:
                        print("{0:<30} {1:>15} ({2})".format(label, v, type(v)))
