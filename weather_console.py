import re
import weather_units
from datetime import datetime


def format_long_date(datetime):
    dayofweek = "{:%A}".format(datetime)
    month = "{:%B}".format(datetime)
    dayofmonth = "{:%d}".format(datetime).lstrip('0')
    year = "{:%Y}".format(datetime)
    return ("{dayofweek} {month} {dayofmonth}, {year}"
        .format(dayofweek=dayofweek, month=month, dayofmonth=dayofmonth, year=year))

def format_long_time(datetime):
    hour = "{:%I}".format(datetime).lstrip('0')
    minutes = "{:%M}".format(datetime)
    ampm = "{:%p}".format(datetime)
    timezone = "{:%Z}".format(datetime)
    return ("{hour}:{minutes} {ampm} {timezone}"
        .format(hour=hour, minutes=minutes, ampm=ampm, timezone=timezone))

def format_short_date(datetime):
    dayofweek = "{:%a}".format(datetime)
    month = "{:%b}".format(datetime)
    dayofmonth = "{:%d}".format(datetime).lstrip('0')
    month_dayofmonth = ("{month} {dayofmonth}"
        .format(month=month, dayofmonth=dayofmonth))
    return {'dayofweek': dayofweek, 'month_dayofmonth': month_dayofmonth}

def format_short_time(datetime):
    hour = "{:%I}".format(datetime).lstrip('0')
    ampm = "{:%p}".format(datetime)
    return {'hour': hour, 'ampm': ampm}

def format_datapoint(label, value='n/a', unit=' '):
    return ("{0:<18} {1:>10} {2:<10}".format(label, value, unit))

def format_datapoint_time(datetime):
    hour = "{:%I}".format(datetime).lstrip('0')
    minutes = "{:%M}".format(datetime)
    hour_minutes = ("{hour}:{minutes}".format(hour=hour, minutes=minutes))
    ampm = "{:%p}".format(datetime)
    return {'hour_minutes': hour_minutes, 'ampm': ampm}

def display_datablock(timezone, datablock={}):
    for k, v in datablock.items():
        print('-' * 80)
        label = k.replace(k[0], k[0].upper(), 1)
        label = re.findall('[A-Z][^A-Z]*', label)
        label = ' '.join(label) + ':'
        if 'Time' in label:
            datablock_time = datetime.fromtimestamp(v, timezone)
            formatted_datablock_time = "{:%Y-%m-%d %I:%M:%S %p %Z}".format(datablock_time)
            print("{0:<30} {1:>30}".format(label, formatted_datablock_time))
        else:
            print("{0:<30} {1:>30} ({2})".format(label, v, type(v)))
    print('-' * 80)

def display_datablock_array(timezone, datablock_array=[]):
    # for datablock in datablock_array:
    #     print('*' * 80)
    #     self.display_datablock(timezone, datablock)
    for i in range(0, 3):
        print('*' * 80)
        display_datablock(timezone, datablock_array[i])
    print('*' * 80)

def display_shared_currently_today(datablock={}):
    # Display data points common to both current and today's weather:
    # Humidity:      xxx           Pressure:       xxx
    # Dew Point:     xxx           UV Index:       xxx
    # Visibility:    xxx           Cloud Cover:    xxx
    # Wind:          xxx

    label = "Humidity:"
    if 'humidity' in datablock:
        humidity = round(datablock['humidity'] * 100)
        print(format_datapoint(label, humidity, weather_units.us_units['humidity']), end='')
    else:
        print(format_datapoint(label), end='')
    label = "Pressure:"
    if 'pressure' in datablock:
        pressure = round(datablock['pressure'])
        print(format_datapoint(label, pressure, weather_units.us_units['pressure']))
    else:
        print(format_datapoint(label))

    label = "Dew Point:"
    if 'dewPoint' in datablock:
        dew_point = round(datablock['dewPoint'])
        print(format_datapoint(label, dew_point, weather_units.us_units['dewPoint']), end='')
    else:
        print(format_datapoint(label), end='')
    label = "UV Index:"
    if 'uvIndex' in datablock:
        uv_index = datablock['uvIndex']
        print(format_datapoint(label, uv_index, weather_units.us_units['uvIndex']))
    else:
        print(format_datapoint(label))

    label = "Visibility:"
    if 'visibility' in datablock:
        visibility = round(datablock['visibility'])
        print(format_datapoint(label, visibility, weather_units.us_units['visibility']), end='')
    else:
        print(format_datapoint(label), end='')
    label = "Cloud Cover:"
    if 'cloudCover' in datablock:
        cloud_cover = round(datablock['cloudCover'] * 100)
        print(format_datapoint(label, cloud_cover, weather_units.us_units['cloudCover']))
    else:
        print(format_datapoint(label))

    label = "Wind:"
    if 'windSpeed' in datablock:
        wind_speed = round(datablock['windSpeed'])
        if 'windBearing' in datablock:
            wind_bearing = weather_units.calculate_cardinal_direction(datablock['windBearing'])
        else:
            wind_bearing = ''
        wind = ("{0} {1}".format(wind_bearing, wind_speed))
        print(format_datapoint(label, wind, weather_units.us_units['windSpeed']), end='')
    else:
        print(format_datapoint(label), end='')

def display_alerts_count(alerts=[]):
    alerts_count = len(alerts)

    if alerts_count == 0:
        print("There are no weather alerts for your location.")
    elif alerts_count == 1:
        print("!!! There is 1 weather alert for your location. !!!")
    else:
        print("!!! There are {0} weather alerts for your location. !!!"
            .format(alerts_count))
    print()

def display_alerts(location, timezone, alerts=[]):
    print("==================={0}".format('=' * len(location)))
    print("Weather Alerts for {0}".format(location))
    print("==================={0}".format('=' * len(location)))
    print()

    for alert_number, alert in enumerate(alerts, start=1):
        print('*' * 80)
        print("Alert #{0}".format(alert_number))
        print()
        print(alert['severity'].upper(), end=': ')
        print(alert['title'])
        alert_time = datetime.fromtimestamp(alert['time'], timezone)
        print("Effective: {date} {time}"
            .format(date=format_long_date(alert_time),
                time=format_long_time(alert_time)))
        alert_expires = datetime.fromtimestamp(alert['expires'], timezone)
        print("Expires: {date} {time}"
            .format(date=format_long_date(alert_expires),
                time=format_long_time(alert_expires)))
        print()
        print("Regions Affected:", end=' ')
        alert_regions = alert['regions']
        alert_regions_count = len(alert_regions)
        for region_number, region in enumerate(alert_regions, start=1):
            if region_number == alert_regions_count:
                print(region)
            else:
                print(region, end=', ')
        print()
        print("Description:")
        print(alert['description'])
        print("Additional Info: {0}".format(alert['uri']))
        print('*' * 80)
        if alert_number < len(alerts):
            print()
            input("--- Press 'Enter' to display the next alert. --- ")
            print()

def display_currently(location, timezone, currently={}):
    print("===================={0}".format('=' * len(location)))
    print("Current Weather for {0}".format(location))
    print("===================={0}".format('=' * len(location)))
    print()

    # display_datablock(timezone, currently)

    currently_datetime = datetime.fromtimestamp(currently['time'], timezone)

    print("{0:<60}{1:>20}".format(format_long_date(currently_datetime),
                format_long_time(currently_datetime)))

    # Summary block
    # --------------------------------------------------------------------------------
    #     100 °F                Mostly Cloudy                100 % Chance of Sleet
    # --------------------------------------------------------------------------------
    print('-' * 80)
    if 'temperature' in currently:
        temperature = round(currently['temperature'])
        print("    {0:>3} {1:<16}".format(temperature, weather_units.us_units['temperature']), end='')
    if 'summary' in currently:
        summary = currently['summary'].rstrip('.')
        print("{0:^26}".format(summary), end='')
    if 'precipProbability' in currently:
        precip_probability = round(currently['precipProbability'] * 100)
        if 'precipType' in currently:
            precip_type = currently['precipType'].title()
        else:
            precip_type = "Rain"
        precip = ("{0} {1} Chance of {2}"
            .format(precip_probability, weather_units.us_units['precipProbability'], precip_type))
        print("{0:>26}    ".format(precip))
    print('-' * 80)

    # Details block
    display_shared_currently_today(currently)
    label = "Nearest Storm:"
    if 'nearestStormDistance' in currently:
        nearest_storm_distance = round(currently['nearestStormDistance'])
        if 'nearestStormBearing' in currently:
            nearest_storm_bearing = weather_units.calculate_cardinal_direction(currently['nearestStormBearing'])
        else:
            nearest_storm_bearing = ''
        nearest_storm = ("{0} {1}"
            .format(nearest_storm_bearing, nearest_storm_distance))
        print(format_datapoint(label, nearest_storm, weather_units.us_units['nearestStormDistance']))
    else:
        print(format_datapoint(label))

def display_hourly(location, timezone, hourly=[]):
    print("==================={0}".format('=' * len(location)))
    print("Hourly Weather for {0}".format(location))
    print("==================={0}".format('=' * len(location)))
    print()

    # display_datablock_array(timezone, hourly)

    max_hours = min(len(hourly), 24)

    for i in range(0, max_hours):
        hour = hourly[i]
        hour_datetime = datetime.fromtimestamp(hour['time'], timezone)
        hour_date = format_short_date(hour_datetime)
        hour_time = format_short_time(hour_datetime)

        # Summary block
        # --------------------------------------------------------------------------------
        #     Sat Sep 30                 100 °F                  100 % Chance of Sleet
        #     12 PM                                                      Mostly Cloudy
        # --------------------------------------------------------------------------------
        print('-' * 80)
        # row 1
        print("    {0:>3} {1:<23}".format(hour_date['dayofweek'], hour_date['month_dayofmonth']), end='')
        if 'temperature' in hour:
            temperature = round(hour['temperature'])
            print("{0:>3} {1:<2}".format(
                temperature, weather_units.us_units['temperature']), end='')
        if 'precipProbability' in hour:
            precip_probability = round(hour['precipProbability'] * 100)
            if 'precipType' in hour:
                precip_type = hour['precipType'].title()
            else:
                precip_type = "Rain"
            precip = ("{0} {1} Chance of {2}"
                .format(precip_probability, weather_units.us_units['precipProbability'], precip_type))
            print("{0:>39}    ".format(precip))
        # row 2
        print("    {0:>2} {1:<7}".format(hour_time['hour'], hour_time['ampm']), end='')
        if 'summary' in hour:
            summary = hour['summary'].rstrip('.')
            print("{0:>62}    ".format(summary))

        pause = 4
        if (i + 1) % pause == 0 and (i + 1) < max_hours:
            print('-' * 80)
            print()
            input("--- Press 'Enter' to display more hours. --- ")
            print()
    print('-' * 80)

def display_daily(location, timezone, daily=[]):
    print("=================={0}".format('=' * len(location)))
    print("Daily Weather for {0}".format(location))
    print("=================={0}".format('=' * len(location)))
    print()

    # display_datablock_array(timezone, daily)

    max_days = len(daily)

    for i in range(0, max_days):
        day = daily[i]
        day_datetime = datetime.fromtimestamp(day['time'], timezone)
        day_date = format_short_date(day_datetime)

        # Summary block
        # --------------------------------------------------------------------------------
        #     Tue Oct 13        100 °F High / -10 °F Low         100 % Chance of Sleet
        #                  Breezy until afternoon and mostly cloudy throughout the day
        # --------------------------------------------------------------------------------
        print('-' * 80)
        # row 1
        print("    {0:>3} {1:<14}".format(day_date['dayofweek'], day_date['month_dayofmonth']), end='')
        if ('temperatureHigh' in day) and ('temperatureLow' in day):
            temperature_high = round(day['temperatureHigh'])
            temperature_low = round(day['temperatureLow'])
            print("{0:>3} {1:<2} High / {2:>3} {3:<2} Low"
                .format(
                    temperature_high, weather_units.us_units['temperatureHigh'],
                    temperature_low, weather_units.us_units['temperatureLow']), end='')
        if 'precipProbability' in day:
            precip_probability = round(day['precipProbability'] * 100)
            if 'precipType' in day:
                precip_type = day['precipType'].title()
            else:
                precip_type = "Rain"
            precip = ("{0} {1} Chance of {2}"
                .format(precip_probability, weather_units.us_units['precipProbability'], precip_type))
            print("{0:>30}    ".format(precip))
        # row 2
        if 'summary' in day:
            summary = day['summary'].rstrip('.')
            print("    {0:>72}    ".format(summary))

        pause = 4
        if (i + 1) % pause == 0 and (i + 1) < max_days:
            print('-' * 80)
            print()
            input("--- Press 'Enter' to display more days. --- ")
            print()
    print('-' * 80)

def display_today(location, timezone, today={}):
    print("===================={0}".format('=' * len(location)))
    print("Today's Weather for {0}".format(location))
    print("===================={0}".format('=' * len(location)))
    print()

    # display_datablock(timezone, today)

    today_datetime = datetime.fromtimestamp(today['time'], timezone)

    print("{0:<60}".format(format_long_date(today_datetime)))

    # Summary block
    # --------------------------------------------------------------------------------
    #     100 °F High / -10 °F Low                           100 % Chance of Sleet
    #                  Breezy until afternoon and mostly cloudy throughout the day
    # --------------------------------------------------------------------------------
    print('-' * 80)
    # row 1
    if ('temperatureHigh' in today) and ('temperatureLow' in today):
        temperature_high = round(today['temperatureHigh'])
        temperature_low = round(today['temperatureLow'])
        print("    {0:>3} {1:<2} High / {2:>3} {3:<2} Low"
            .format(
                temperature_high, weather_units.us_units['temperatureHigh'],
                temperature_low, weather_units.us_units['temperatureLow']), end='')
    if 'precipProbability' in today:
        precip_probability = round(today['precipProbability'] * 100)
        if 'precipType' in today:
            precip_type = today['precipType'].title()
        else:
            precip_type = "Rain"
        precip = ("{0} {1} Chance of {2}"
            .format(precip_probability, weather_units.us_units['precipProbability'], precip_type))
        print("{0:>48}    ".format(precip))
    # row 2
    if 'summary' in today:
        summary = today['summary'].rstrip('.')
        print("    {0:>72}    ".format(summary))
    print('-' * 80)

    # Details block
    display_shared_currently_today(today)
    label = "Moon Phase:"
    if 'moonPhase' in today:
        moon_phase = weather_units.calculate_moon_phase(today['moonPhase'])
        print(format_datapoint(label, moon_phase[0], moon_phase[1]))
    else:
        print(format_datapoint(label))

    label = "Sunrise:"
    if 'sunriseTime' in today:
        sunrise_datetime = datetime.fromtimestamp(today['sunriseTime'], timezone)
        sunrise_time = format_datapoint_time(sunrise_datetime)
        print(format_datapoint(label, sunrise_time['hour_minutes'], sunrise_time['ampm']), end='')
    else:
        print(format_datapoint(label), end='')
    label = "Sunset:"
    if 'sunsetTime' in today:
        sunset_datetime = datetime.fromtimestamp(today['sunsetTime'], timezone)
        sunset_time = format_datapoint_time(sunset_datetime)
        print(format_datapoint(label, sunset_time['hour_minutes'], sunset_time['ampm']))
    else:
        print(format_datapoint(label))
