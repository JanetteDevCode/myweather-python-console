from api_request import ApiRequest


class WeatherApiRequest:
    darksky_api_key = '7f560844e81c036d5e8beafb449eda24'

    @classmethod
    def get_darksky_uri(cls, latitude, longitude):
        return ('https://api.darksky.net/forecast/'
            + WeatherApiRequest.darksky_api_key + '/'
            + str(latitude) + ',' + str(longitude))

    @classmethod
    def get_current_weather_json(cls, latitude, longitude):
        exclude = 'minutely,hourly,daily,flags'
        return ApiRequest.make_api_request(
                cls.get_darksky_uri(latitude, longitude),
                {'exclude': exclude}
            )
