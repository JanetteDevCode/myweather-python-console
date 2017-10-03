import os
from api_request import ApiRequest


class WeatherApiRequest:
    try:
        api_key = os.environ['DARKSKY_API_KEY']
    except:
        api_key = None

    @classmethod
    def get_darksky_uri(cls, api_key, latitude, longitude):
        return ('https://api.darksky.net/forecast/'
            + api_key + '/'
            + str(latitude) + ',' + str(longitude))

    @classmethod
    def get_weather_alerts(cls, latitude, longitude):
        exclude = 'currently,minutely,hourly,daily,flags'
        if WeatherApiRequest.api_key:
            return ApiRequest.make_api_request(
                    cls.get_darksky_uri(WeatherApiRequest.api_key, latitude, longitude),
                    {'exclude': exclude}
                )
        else:
            return {'status': 'ERROR',
                'error': "An API key for the Dark Sky API is required."}

    @classmethod
    def get_current_weather_json(cls, latitude, longitude):
        exclude = 'minutely,hourly,daily,flags'
        if WeatherApiRequest.api_key:
            return ApiRequest.make_api_request(
                    cls.get_darksky_uri(WeatherApiRequest.api_key, latitude, longitude),
                    {'exclude': exclude}
                )
        else:
            return {'status': 'ERROR',
                'error': "An API key for the Dark Sky API is required."}

    @classmethod
    def get_hourly_weather_json(cls, latitude, longitude):
        exclude = 'currently,minutely,daily,flags'
        if WeatherApiRequest.api_key:
            return ApiRequest.make_api_request(
                    cls.get_darksky_uri(WeatherApiRequest.api_key, latitude, longitude),
                    {'exclude': exclude}
                )
        else:
            return {'status': 'ERROR',
                'error': "An API key for the Dark Sky API is required."}

    @classmethod
    def get_daily_weather_json(cls, latitude, longitude):
        exclude = 'currently,minutely,hourly,flags'
        if WeatherApiRequest.api_key:
            return ApiRequest.make_api_request(
                    cls.get_darksky_uri(WeatherApiRequest.api_key, latitude, longitude),
                    {'exclude': exclude}
                )
        else:
            return {'status': 'ERROR',
                'error': "An API key for the Dark Sky API is required."}
