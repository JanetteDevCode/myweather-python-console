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

            # print()
            # print("Latitude: {0}, Longitude: {1}".format(
            #         weather_json['latitude'],
            #         weather_json['longitude'])
            #     )
            # print("Timezone:", weather_timezone.zone)

            if 'alerts' in weather_json:
                self.display_alerts(weather_timezone, weather_json['alerts'])

            if 'currently' in weather_json:
                self.display_currently(weather_timezone, weather_json['currently'])

    def display_datablock(self, timezone, datablock={}):
        print('-' * 80)
        for k, v in datablock.items():
            label = k.replace(k[0], k[0].upper(), 1)
            label = re.findall('[A-Z][^A-Z]*', label)
            label = ' '.join(label) + ':'
            if 'Time' in label:
                datablock_time = datetime.fromtimestamp(v, timezone)
                formatted_datablock_time = "{:%Y-%m-%d %I:%M:%S %p %Z}".format(datablock_time)
                print("{0:<30} {1:>30}".format(label, formatted_datablock_time))
            else:
                print("{0:<30} {1:>30} ({2})".format(label, v, type(v)))
            print('-' * 80)

    def display_alerts(self, timezone, alerts={}):
        print()
        print("==================={0}".format('=' * len(self.__zip_code)))
        print("Weather Alerts for {0}".format(self.__zip_code))
        print("==================={0}".format('=' * len(self.__zip_code)))
        print()

        for i, alert in enumerate(alerts, start=1):
            print('*' * 80)
            print("Alert #{0}".format(i))
            print()
            print(alert['severity'].upper(), end=': ')
            print(alert['title'])
            alert_time = datetime.fromtimestamp(alert['time'], timezone)
            print("Issued at: {:%Y-%m-%d %I:%M:%S %p %Z}".format(alert_time))
            alert_expires = datetime.fromtimestamp(alert['expires'], timezone)
            print("Expires at: {:%Y-%m-%d %I:%M:%S %p %Z}".format(alert_expires))
            print()
            print("Regions affected:", end=' ')
            alert_regions = alert['regions']
            alert_regions_count = len(alert_regions)
            for i, region in enumerate(alert_regions, start=1):
                if i == alert_regions_count:
                    print(region)
                else:
                    print(region, end=', ')
            print()
            print("Description:")
            print(alert['description'])
            print("Additional Info: {0}".format(alert['uri']))
        print('*' * 80)

    def display_currently(self, timezone, currently={}):
        print()
        print("===================={0}".format('=' * len(self.__zip_code)))
        print("Current Weather for {0}".format(self.__zip_code))
        print("===================={0}".format('=' * len(self.__zip_code)))
        print()

        self.display_datablock(timezone, currently)
