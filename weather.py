import re
from datetime import datetime
from pytz import timezone
from weather_api_request import WeatherApiRequest


class Weather:
    def __init__(self, zip_code, latitude, longitude):
        self.__zip_code = zip_code
        self.__latitude = latitude
        self.__longitude = longitude

    def get_weather_alerts(self):
        weather_json = WeatherApiRequest.get_weather_alerts(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            print("Error! Could not retrieve weather alerts.")
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                self.display_alerts(weather_timezone, weather_json['alerts'])
            else:
                print("There are no weather alerts for your location.")

    def get_current_weather(self):
        weather_json = WeatherApiRequest.get_current_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            print("Error! Could not retrieve current weather data.")
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                self.display_alerts_count(weather_json['alerts'])

            if 'currently' in weather_json:
                self.display_currently(weather_timezone, weather_json['currently'])

    def get_hourly_weather(self):
        weather_json = WeatherApiRequest.get_hourly_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            print("Error! Could not retrieve hourly weather data.")
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                self.display_alerts_count(weather_json['alerts'])

            if 'hourly' in weather_json:
                self.display_hourly(weather_timezone, weather_json['hourly']['data'])

    def get_daily_weather(self):
        weather_json = WeatherApiRequest.get_daily_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            print("Error! Could not retrieve daily weather data.")
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                self.display_alerts_count(weather_json['alerts'])

            if 'daily' in weather_json:
                self.display_daily(weather_timezone, weather_json['daily']['data'])

    def get_today_weather(self):
        weather_json = WeatherApiRequest.get_daily_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            print("Error! Could not retrieve daily weather data.")
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                self.display_alerts_count(weather_json['alerts'])

            if 'daily' in weather_json:
                self.display_today(weather_timezone, weather_json['daily']['data'][0])

    def display_datablock(self, timezone, datablock={}):
        for k, v in datablock.items():
            print('-' * 80)
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

    def display_datablock_array(self, timezone, datablock_array=[]):
        # for datablock in datablock_array:
        #     print('*' * 80)
        #     self.display_datablock(timezone, datablock)
        for i in range(0, 3):
            print('*' * 80)
            self.display_datablock(timezone, datablock_array[i])
        print('*' * 80)

    def display_alerts_count(self, alerts=[]):
        alerts_count = len(alerts)

        if alerts_count == 0:
            print("There are no weather alerts for your location.")
        elif alerts_count == 1:
            print("!!! There is 1 weather alert for your location. !!!")
        else:
            print("!!! There are {0} weather alerts for your location. !!!"
                .format(alerts_count))

    def display_alerts(self, timezone, alerts=[]):
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

    def display_hourly(self, timezone, hourly=[]):
        print()
        print("==================={0}".format('=' * len(self.__zip_code)))
        print("Hourly Weather for {0}".format(self.__zip_code))
        print("==================={0}".format('=' * len(self.__zip_code)))
        print()

        self.display_datablock_array(timezone, hourly)

    def display_daily(self, timezone, daily=[]):
        print()
        print("=================={0}".format('=' * len(self.__zip_code)))
        print("Daily Weather for {0}".format(self.__zip_code))
        print("=================={0}".format('=' * len(self.__zip_code)))
        print()

        self.display_datablock_array(timezone, daily)

    def display_today(self, timezone, today={}):
        print()
        print("===================={0}".format('=' * len(self.__zip_code)))
        print("Today's Weather for {0}".format(self.__zip_code))
        print("===================={0}".format('=' * len(self.__zip_code)))
        print()

        self.display_datablock(timezone, today)
