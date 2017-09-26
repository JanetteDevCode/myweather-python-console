import json, requests


class ApiRequest:
    @classmethod
    def make_api_request(cls, uri='', params={}, timeout=10):
        try:
            req = requests.get(uri, params=params, timeout=timeout)
            # print(req.url)
            return req.json()
        except Exception as e:
            return {'error': e}
