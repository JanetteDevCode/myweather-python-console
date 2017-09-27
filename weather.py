import math, re
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

    def calculate_cardinal_direction(self, angle):
        cardinal_directions = [
            "N", # 0: < 11.25, >= 348.75
            "NNE", # 1: < 33.75
            "NE", # 2: < 56.25
            "ENE", # 3: < 78.75
            "E", # 4: < 101.25
            "ESE", # 5: < 123.75
            "SE", # 6: < 146.25
            "SSE", # 7: < 168.75
            "S", # 8: < 191.25
            "SSW", # 9: < 213.75
            "SW", # 10: < 236.25
            "WSW", # 11: < 258.75
            "W", # 12: < 281.25
            "WNW", # 13: < 303.75
            "NW", # 14: < 326.25
            "NNW" # 15: < 348.75
        ]

        if isinstance(angle, float) or isinstance(angle, int):
            i = math.floor(angle / 22.5 + 0.5) % 16
            return cardinal_directions[i]
        else:
            return ''

    def format_long_date(self, datetime):
        dayofweek = "{:%A}".format(datetime)
        month = "{:%B}".format(datetime)
        dayofmonth = "{:%d}".format(datetime).lstrip('0')
        year = "{:%Y}".format(datetime)
        return ("{dayofweek} {month} {dayofmonth}, {year}"
            .format(dayofweek=dayofweek, month=month, dayofmonth=dayofmonth, year=year))

    def format_long_time(self, datetime):
        hour = "{:%I}".format(datetime).lstrip('0')
        minutes = "{:%M}".format(datetime)
        ampm = "{:%p}".format(datetime)
        timezone = "{:%Z}".format(datetime)
        return ("{hour}:{minutes} {ampm} {timezone}"
            .format(hour=hour, minutes=minutes, ampm=ampm, timezone=timezone))

    def format_datapoint(self, label, value='n/a', unit=' '):
        return ("{0:<18} {1:>10} {2:<10}".format(label, value, unit))

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
            print("Issued at: {date} {time}"
                .format(date=self.format_long_date(alert_time),
                    time=self.format_long_time(alert_time)))
            alert_expires = datetime.fromtimestamp(alert['expires'], timezone)
            print("Expires at: {date} {time}"
                .format(date=self.format_long_date(alert_expires),
                    time=self.format_long_time(alert_expires)))
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
            if i < len(alerts):
                print()
                input("--- Press 'Enter' to display the next alert. --- ")
                print()

    def display_currently(self, timezone, currently={}):
        print()
        print("===================={0}".format('=' * len(self.__zip_code)))
        print("Current Weather for {0}".format(self.__zip_code))
        print("===================={0}".format('=' * len(self.__zip_code)))
        print()

        # self.display_datablock(timezone, currently)

        currently_datetime = datetime.fromtimestamp(currently['time'], timezone)

        print("{0:<60}{1:>20}".format(self.format_long_date(currently_datetime),
                    self.format_long_time(currently_datetime)))

        # Summary block
        # temperature    summary    precip
        print('-' * 80)
        if 'temperature' in currently:
            temperature = round(currently['temperature'])
            print("    {0:>3} {1:<16}".format(temperature, '\u00b0F'), end='')
        if 'summary' in currently:
            summary = currently['summary']
            print("{0:^26}".format(summary), end='')
        # precip
        if 'precipProbability' in currently:
            precip_probability = round(currently['precipProbability'] * 100)
            if 'precipType' in currently:
                precip_type = currently['precipType'].title()
            else:
                precip_type = "Rain"
            precip = ("{0} {1} Chance of {2}"
                .format(precip_probability, '%', precip_type))
            print("{0:>26}    ".format(precip))
        print('-' * 80)

        # Details block
        # humidity    pressure
        label = "Humidity:"
        if 'humidity' in currently:
            humidity = round(currently['humidity'] * 100)
            print(self.format_datapoint(label, humidity, '%'), end='')
        else:
            print(self.format_datapoint(label), end='')
        label = "Pressure:"
        if 'pressure' in currently:
            pressure = round(currently['pressure'])
            print(self.format_datapoint(label, pressure, 'mbar'))
        else:
            print(self.format_datapoint(label))

        # dew_point    uv_index
        label = "Dew Point:"
        if 'dewPoint' in currently:
            dew_point = round(currently['dewPoint'])
            print(self.format_datapoint(label, dew_point, '\u00b0F'), end='')
        else:
            print(self.format_datapoint(label), end='')
        label = "UV Index:"
        if 'uvIndex' in currently:
            uv_index = currently['uvIndex']
            print(self.format_datapoint(label, uv_index, ''))
        else:
            print(self.format_datapoint(label))

        # visibility    cloud_cover
        label = "Visibility:"
        if 'visibility' in currently:
            visibility = round(currently['visibility'])
            print(self.format_datapoint(label, visibility, 'mi'), end='')
        else:
            print(self.format_datapoint(label), end='')
        label = "Cloud Cover:"
        if 'cloudCover' in currently:
            cloud_cover = round(currently['cloudCover'] * 100)
            print(self.format_datapoint(label, cloud_cover, '%'))
        else:
            print(self.format_datapoint(label))

        # wind    nearest_storm
        label = "Wind:"
        if 'windSpeed' in currently:
            wind_speed = round(currently['windSpeed'])
            if 'windBearing' in currently:
                wind_bearing = self.calculate_cardinal_direction(currently['windBearing'])
            else:
                wind_bearing = ''
            wind = ("{0} {1}".format(wind_bearing, wind_speed))
            print(self.format_datapoint(label, wind, 'mph'), end='')
        else:
            print(self.format_datapoint(label), end='')
        label = "Nearest Storm:"
        if 'nearestStormDistance' in currently:
            nearest_storm_distance = round(currently['nearestStormDistance'])
            if 'nearestStormBearing' in currently:
                nearest_storm_bearing = self.calculate_cardinal_direction(currently['nearestStormBearing'])
            else:
                nearest_storm_bearing = ''
            nearest_storm = ("{0} {1}"
                .format(nearest_storm_bearing, nearest_storm_distance))
            print(self.format_datapoint(label, nearest_storm, 'mi'))
        else:
            print(self.format_datapoint(label))
        print()

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
