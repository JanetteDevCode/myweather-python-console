import math


us_units = {
    'cloudCover': '%',
    'dewPoint': '\u00b0F',
    'humidity': '%',
    'moonPhase': ' ',
    'nearestStormDistance': 'mi',
    'precipProbability': '%',
    'pressure': 'mbar',
    'temperature': '\u00b0F',
    'temperatureHigh': '\u00b0F',
    'temperatureLow': '\u00b0F',
    'visibility': 'mi',
    'uvIndex': ' ',
    'windSpeed': 'mph'
}

def calculate_cardinal_direction(angle):
    cardinal_directions = [
        "N", # 0: < 11.25, >= 348.75
        "NNE", # 1: < 33.75
        "NE", # 2: < 56.25
        "ENE", # 3: < 78.75
        "E", # 4: < 101.25
        "ESE", # 5: < 123.75
        "SE", # 6: < 146.25
        "SSE", # 7: < 168.75
        "S", # 8: < 191.25
        "SSW", # 9: < 213.75
        "SW", # 10: < 236.25
        "WSW", # 11: < 258.75
        "W", # 12: < 281.25
        "WNW", # 13: < 303.75
        "NW", # 14: < 326.25
        "NNW" # 15: < 348.75
    ]

    if isinstance(angle, float) or isinstance(angle, int):
        i = math.floor(angle / 22.5 + 0.5) % 16
        return cardinal_directions[i]
    else:
        return ''

def calculate_moon_phase(lunation_fraction):
    if not (isinstance(lunation_fraction, float) or isinstance(lunation_fraction, int)):
        return ['', '']

    if lunation_fraction == 0:
        return ["new", "moon"]
    elif lunation_fraction < 0.25:
        return ["waxing", "crescent"]
    elif lunation_fraction == 0.25:
        return ["first", "quarter"]
    elif lunation_fraction < 0.5:
        return ["waxing", "gibbous"]
    elif lunation_fraction == 0.5:
        return ["full", "moon"]
    elif lunation_fraction < 0.75:
        return ["waning", "gibbous"]
    elif lunation_fraction == 0.75:
        return ["last", "quarter"]
    elif lunation_fraction > 0.75:
        return ["waning", "crescent"]
