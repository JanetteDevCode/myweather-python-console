from api_request import ApiRequest


class GeocodeApiRequest:
    googlemapsgeocoding_api_key = 'AIzaSyBO5h570rjeDP9Cz8KkCeAFwX-NHu0fLkQ'

    @classmethod
    def get_googlemapsgeocoding_uri(cls):
        return ('https://maps.googleapis.com/maps/api/geocode/json')

    @classmethod
    def get_geocode_json(cls, zip_code):
        return ApiRequest.make_api_request(
                cls.get_googlemapsgeocoding_uri(),
                {'components': 'postal_code:' + zip_code,
                'key': GeocodeApiRequest.googlemapsgeocoding_api_key}
            )
