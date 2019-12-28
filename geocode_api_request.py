import os
from api_request import ApiRequest


class GeocodeApiRequest:
    try:
        api_key = os.environ['MAPQUEST_OPEN_GEOCODING_API_KEY']
    except:
        api_key = None

    @classmethod
    def get_openmapquest_geocoding_uri(cls):
        return ('http://open.mapquestapi.com/geocoding/v1/address')

    @classmethod
    def get_geocode_json(cls, location):
        if GeocodeApiRequest.api_key:
            return ApiRequest.make_api_request(
                cls.get_openmapquest_geocoding_uri(),
                params={ 'location': str(location),
                         'key': GeocodeApiRequest.api_key }
            )
        else:
            return { 'status': 'ERROR',
                     'error': "An API key for the MapQuest Open Geocoding API is required." }
