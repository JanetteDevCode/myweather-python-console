import os
from api_request import ApiRequest


class GeocodeApiRequest:
    try:
        api_key = os.environ['GOOGLEMAPS_GEOCODING_API_KEY']
    except:
        api_key = None

    @classmethod
    def get_googlemapsgeocoding_uri(cls):
        return ('https://maps.googleapis.com/maps/api/geocode/json')

    @classmethod
    def get_geocode_json(cls, zip_code):
        if GeocodeApiRequest.api_key:
            return ApiRequest.make_api_request(
                    cls.get_googlemapsgeocoding_uri(),
                    {'components': 'postal_code:' + zip_code,
                    'key': GeocodeApiRequest.api_key}
                )
        else:
            return {'status': 'ERROR',
                'error': "An API key for the Google Maps Geocoding API is required."}
