from geocode_api_request import GeocodeApiRequest


class Geocode:
    @classmethod
    def get_locations(cls, address, country='US'):
        geocode_json = GeocodeApiRequest.get_geocode_json(address)

        results = {
            'status': '',
            'error': '',
            'locations': '',
        }

        if geocode_json['info']['statuscode'] != 0:
            results['status'] = 'ERROR'
            results['error'] = ("Error! Could not retrieve geocode data.")
        else:
            locations = list(filter(
                    lambda location: location['adminArea1'] == country, 
                    geocode_json['results'][0]['locations']
                )
            )
            # print(locations)
            results['status'] = 'OK'
            results['locations'] = locations

        return results
