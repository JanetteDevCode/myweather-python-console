import weather_console
from pytz import timezone
from weather_api_request import WeatherApiRequest


class Weather:
    def __init__(self, zip_code, latitude, longitude):
        self.__zip_code = zip_code
        self.__latitude = latitude
        self.__longitude = longitude

    def get_weather_alerts(self):
        status = {'status': 'OK', 'error_message': ''}
        weather_json = WeatherApiRequest.get_weather_alerts(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            error_message = ("Error! Could not retrieve weather alerts.")
            status = {'status': 'ERROR', 'error_message': error_message}
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                weather_console.display_alerts(
                    self.__zip_code, weather_timezone, weather_json['alerts'])
            else:
                error_message = ("There are no weather alerts for your location.")
                status = {'status': 'ERROR', 'error_message': error_message}

        return status

    def get_current_weather(self):
        status = {'status': 'OK', 'error_message': ''}
        weather_json = WeatherApiRequest.get_current_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            error_message = ("Error! Could not retrieve current weather data.")
            status = {'status': 'ERROR', 'error_message': error_message}
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                weather_console.display_alerts_count(weather_json['alerts'])

            if 'currently' in weather_json:
                weather_console.display_currently(
                    self.__zip_code, weather_timezone, weather_json['currently'])

        return status

    def get_hourly_weather(self):
        status = {'status': 'OK', 'error_message': ''}
        weather_json = WeatherApiRequest.get_hourly_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            error_message = ("Error! Could not retrieve hourly weather data.")
            status = {'status': 'ERROR', 'error_message': error_message}
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                weather_console.display_alerts_count(weather_json['alerts'])

            if 'hourly' in weather_json:
                weather_console.display_hourly(
                    self.__zip_code, weather_timezone, weather_json['hourly']['data'])

        return status

    def get_daily_weather(self):
        status = {'status': 'OK', 'error_message': ''}
        weather_json = WeatherApiRequest.get_daily_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            error_message = ("Error! Could not retrieve daily weather data.")
            status = {'status': 'ERROR', 'error_message': error_message}
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                weather_console.display_alerts_count(weather_json['alerts'])

            if 'daily' in weather_json:
                weather_console.display_daily(
                    self.__zip_code, weather_timezone, weather_json['daily']['data'])

        return status

    def get_today_weather(self):
        status = {'status': 'OK', 'error_message': ''}
        weather_json = WeatherApiRequest.get_daily_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            error_message = ("Error! Could not retrieve today's weather data.")
            status = {'status': 'ERROR', 'error_message': error_message}
        else:
            weather_timezone = timezone(weather_json['timezone'])

            if 'alerts' in weather_json:
                weather_console.display_alerts_count(weather_json['alerts'])

            if 'daily' in weather_json:
                weather_console.display_today(
                    self.__zip_code, weather_timezone, weather_json['daily']['data'][0])

        return status
