from weather_api_request import WeatherApiRequest


class Weather:
    def __init__(self, location, latitude, longitude):
        self.__location = location
        self.__latitude = latitude
        self.__longitude = longitude

    def get_weather_alerts(self):
        results = {
            'status': '',
            'error': '',
            'location': '',
            'timezone': '',
            'alerts': []
        }
        weather_json = WeatherApiRequest.get_weather_alerts(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            results['status'] = 'ERROR'
            results['error'] = ("Error! Could not retrieve weather alerts.")
            results['error'] += ("\n" + weather_json['error'])
        else:
            if 'alerts' in weather_json:
                results['status'] = 'OK'
                results['alerts'] = weather_json['alerts']
                results['location'] = self.__location
                results['timezone'] = weather_json['timezone']
            else:
                results['status'] = 'ERROR'
                results['error'] = ("There are no weather alerts for your location.")

        return results

    def get_current_weather(self):
        results = {
            'status': '',
            'error': '',
            'location': '',
            'timezone': '',
            'alerts': [],
            'currently': {}
        }
        weather_json = WeatherApiRequest.get_current_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            results['status'] = 'ERROR'
            results['error'] = ("Error! Could not retrieve current weather data.")
            results['error'] += ("\n" + weather_json['error'])
        else:
            if 'currently' in weather_json:
                results['status'] = 'OK'
                results['currently'] = weather_json['currently']
                results['location'] = self.__location
                results['timezone'] = weather_json['timezone']
                if 'alerts' in weather_json:
                    results['alerts'] = weather_json['alerts']
            else:
                results['status'] = 'ERROR'
                results['error'] = ("There are no current weather data for your location.")

        return results

    def get_hourly_weather(self):
        results = {
            'status': '',
            'error': '',
            'location': '',
            'timezone': '',
            'alerts': [],
            'hourly': []
        }
        weather_json = WeatherApiRequest.get_hourly_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            results['status'] = 'ERROR'
            results['error'] = ("Error! Could not retrieve hourly weather data.")
            results['error'] += ("\n" + weather_json['error'])
        else:
            if 'hourly' in weather_json:
                results['status'] = 'OK'
                results['hourly'] = weather_json['hourly']['data']
                results['location'] = self.__location
                results['timezone'] = weather_json['timezone']
                if 'alerts' in weather_json:
                    results['alerts'] = weather_json['alerts']
            else:
                results['status'] = 'ERROR'
                results['error'] = ("There are no hourly weather data for your location.")

        return results

    def get_daily_weather(self):
        results = {
            'status': '',
            'error': '',
            'location': '',
            'timezone': '',
            'alerts': [],
            'daily': []
        }
        weather_json = WeatherApiRequest.get_daily_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            results['status'] = 'ERROR'
            results['error'] = ("Error! Could not retrieve daily weather data.")
            results['error'] += ("\n" + weather_json['error'])
        else:
            if 'daily' in weather_json:
                results['status'] = 'OK'
                results['daily'] = weather_json['daily']['data']
                results['location'] = self.__location
                results['timezone'] = weather_json['timezone']
                if 'alerts' in weather_json:
                    results['alerts'] = weather_json['alerts']
            else:
                results['status'] = 'ERROR'
                results['error'] = ("There are no daily weather data for your location.")

        return results

    def get_today_weather(self):
        results = {
            'status': '',
            'error': '',
            'location': '',
            'timezone': '',
            'alerts': [],
            'today': {}
        }
        weather_json = WeatherApiRequest.get_daily_weather_json(
            self.__latitude, self.__longitude)

        if 'error' in weather_json:
            results['status'] = 'ERROR'
            results['error'] = ("Error! Could not retrieve today's weather data.")
            results['error'] += ("\n" + weather_json['error'])
        else:
            if 'daily' in weather_json:
                results['status'] = 'OK'
                results['today'] = weather_json['daily']['data'][0]
                results['location'] = self.__location
                results['timezone'] = weather_json['timezone']
                if 'alerts' in weather_json:
                    results['alerts'] = weather_json['alerts']
            else:
                results['status'] = 'ERROR'
                results['error'] = ("There are no today's weather data for your location.")

        return results
