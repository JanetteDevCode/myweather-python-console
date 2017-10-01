import os
from api_request import ApiRequest


class WeatherApiRequest:
    darksky_api_key = os.environ['DARKSKY_API_KEY']

    @classmethod
    def get_darksky_uri(cls, latitude, longitude):
        return ('https://api.darksky.net/forecast/'
            + WeatherApiRequest.darksky_api_key + '/'
            + str(latitude) + ',' + str(longitude))

    @classmethod
    def get_weather_alerts(cls, latitude, longitude):
        exclude = 'currently,minutely,hourly,daily,flags'
        return ApiRequest.make_api_request(
                cls.get_darksky_uri(latitude, longitude),
                {'exclude': exclude}
            )

    @classmethod
    def get_current_weather_json(cls, latitude, longitude):
        exclude = 'minutely,hourly,daily,flags'
        return ApiRequest.make_api_request(
                cls.get_darksky_uri(latitude, longitude),
                {'exclude': exclude}
            )

    @classmethod
    def get_hourly_weather_json(cls, latitude, longitude):
        exclude = 'currently,minutely,daily,flags'
        return ApiRequest.make_api_request(
                cls.get_darksky_uri(latitude, longitude),
                {'exclude': exclude}
            )

    @classmethod
    def get_daily_weather_json(cls, latitude, longitude):
        exclude = 'currently,minutely,hourly,flags'
        return ApiRequest.make_api_request(
                cls.get_darksky_uri(latitude, longitude),
                {'exclude': exclude}
            )
