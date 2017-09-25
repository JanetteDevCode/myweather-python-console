import datetime, json, pytz, re, requests, sys


class ApiRequest:
    @classmethod
    def make_api_request(cls, uri='', params={}, timeout=10):
        try:
            req = requests.get(uri, params=params, timeout=timeout)
            # print(req.url)
            return req.json()
        except Exception as e:
            return {'error': e}


class Geocode:
    googlemapsgeocoding_api_key = 'AIzaSyBO5h570rjeDP9Cz8KkCeAFwX-NHu0fLkQ'

    @classmethod
    def get_googlemapsgeocoding_uri(cls):
        return ('https://maps.googleapis.com/maps/api/geocode/json')

    @classmethod
    def get_geocode_json(cls, zip_code):
        return ApiRequest.make_api_request(
                cls.get_googlemapsgeocoding_uri(),
                {'components': 'postal_code:' + zip_code,
                'key': Geocode.googlemapsgeocoding_api_key}
            )


class Weather:
    darksky_api_key = '7f560844e81c036d5e8beafb449eda24'

    @classmethod
    def get_darksky_uri(cls, latitude, longitude):
        return ('https://api.darksky.net/forecast/'
            + Weather.darksky_api_key + '/'
            + str(latitude) + ',' + str(longitude))

    @classmethod
    def get_current_weather_json(cls, latitude, longitude):
        exclude = 'minutely,hourly,daily,flags'
        return ApiRequest.make_api_request(
                cls.get_darksky_uri(latitude, longitude),
                {'exclude': exclude}
            )


print("-----------------------------")
print("---- My Weather Forecast ----")
print("-----------------------------")
print()

zip_code = input("Enter ZIP code: ")
geocode_json = Geocode.get_geocode_json(zip_code)

if geocode_json['status'] != 'OK' or 'error' in geocode_json:
    print("Error! Could not retrieve geocode data.")
    sys.exit()
else:
    latitude = geocode_json['results'][0]['geometry']['location']['lat']
    longitude = geocode_json['results'][0]['geometry']['location']['lng']
    print()
    print("ZIP Code: {0}".format(zip_code))
    print("Latitude: {0}, Longitude: {1}".format(latitude, longitude))

current_weather_json = Weather.get_current_weather_json(latitude, longitude)

print()
print("Current Weather for {0}".format(zip_code))
print("--------------------{0}".format('-' * len(zip_code)))
print()

if 'error' in current_weather_json:
    print("Error! Could not retrieve current weather data.")
else:
    print("Latitude: {0}, Longitude: {1}".format(
            current_weather_json['latitude'],
            current_weather_json['longitude'])
        )
    timezone = current_weather_json['timezone']
    tz = pytz.timezone(timezone)
    print("Timezone: {0}".format(timezone))
    if 'alerts' in current_weather_json:
        for i, v in enumerate(current_weather_json['alerts'], start=1):
            print('*' * 80)
            print("Alert #{0}".format(i))
            print(v['severity'].upper(), end=': ')
            print(v['title'])
            dt = datetime.datetime.fromtimestamp(v['time'])
            dt_aware = tz.localize(dt)
            print("Issued at: {:%Y-%m-%d %I:%M:%S %p %Z}".format(dt_aware))
            dt = datetime.datetime.fromtimestamp(v['expires'])
            dt_aware = tz.localize(dt)
            print("Expires at: {:%Y-%m-%d %I:%M:%S %p %Z}".format(dt_aware))
            print("Regions affected:", end=' ')
            regions = v['regions']
            regions_count = len(regions)
            for i, r in enumerate(regions, start=1):
                if i == regions_count:
                    print(r)
                else:
                    print(r, end=', ')
            print("Description:")
            print(v['description'])
        print('*' * 80)
    if 'currently' in current_weather_json:
        for k, v in current_weather_json['currently'].items():
            label = k.replace(k[0], k[0].upper(), 1)
            label = re.findall('[A-Z][^A-Z]*', label)
            label = ' '.join(label) + ':'
            if k == 'time':
                dt = datetime.datetime.fromtimestamp(v)
                dt_aware = tz.localize(dt)
                print("Date: {:%Y-%m-%d}".format(dt_aware))
                print("Time: {:%I:%M:%S %p %Z}".format(dt_aware))
            else:
                print("{0:<30} {1:>15} ({2})".format(label, v, type(v)))
