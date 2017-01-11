# -*- coding: utf-8-*-
import requests
import sys
import json

###############################
# DarkSky forecast request
class DarkSky(object):
    """
    DarkSky forecasts main class
    """

    ###############################
    # Initialize
    def __init__(self, api_key, location_lat='', location_long='', units='si', exclude='minutely,hourly'):
        """
        Initialize DarkSky class, building the full URL
        """

        if (api_key is None or location_lat is None or location_long is None):
            print('Required parameters missing')
            sys.exit(1)

        self.api_key = api_key
        self.units = units
        self.exclude = exclude
        self.location_lat = location_lat
        self.location_long = location_long
        self.raw_response = ''
        self.forecast_response = ''

        self.url = 'https://api.darksky.net/forecast/'
        self.url += self.api_key
        self.url += '/' + self.location_lat
        self.url += ',' + self.location_long
        self.url += '?units=' + self.units
        if len(exclude) > 0:
            self.url += '&exclude=' + self.exclude

    ###############################
    # Get Forecast from DakSky
    def get_forecast(self):
        """
        GET json response forecast for a given location
        """

        try:

            headers = {'content-type': 'application/x-www-form-urlencoded',
                       'accept': 'application/json'}
            response = requests.get(self.url, headers=headers, verify=False)

        except requests.exceptions.Timeout as ext:
            print('Error: Timeout', ext)
        except requests.exceptions.TooManyRedirects as extmr:
            print('Error: TooManyRedirects', extmr)
        except requests.exceptions.RequestException as ex:
            print('Error: RequestException', ex)
            sys.exit(1)

        try:
            self.cache_control = response.headers['Cache-Control']
        except KeyError as kerr:
            print('Warning: Could not get headers. %s' % kerr)
            self.cache_control = None
        try:
            self.expires = response.headers['Expires']
        except KeyError as kerr:
            print('Warning: Could not get headers. %s' % kerr)
            self.extend_url = None
        try:
            self.x_forecast_api_calls = response.headers['X-Forecast-API-Calls']
        except KeyError as kerr:
            print('Warning: Could not get headers. %s' % kerr)
            self.x_forecast_api_calls = None
        try:
            self.x_responde_time = response.headers['X-Response-Time']
        except KeyError as kerr:
            print('Warning: Could not get headers. %s' % kerr)
            self.x_responde_time = None

        if response.status_code is not 200:
            raise requests.exceptions.HTTPError('Bad response, status code: %x' % (response.status_code))


        self.raw_response = response.text
        self.json_response = json.loads(response.text)



    ###############################
    # Make the forecast huma readable
    def get_pretty_summary(self, when='today'):
        """
        Process DarkSky response (json) and make it more human readable
        """

        valid_periods = ['today', 'tomorrow', 1, 2, 3, 4, 5, 6, 7]

        if when not in valid_periods:
            when = 'today'
        elif when == 'tomorrow':
            when = 1

        self.when = when


        if self.when == 'today':
            temp_current = self.json_response['currently']['temperature']
            temp_feelslike = self.json_response['currently']['apparentTemperature']
            summary_now = self.json_response['currently']['summary']
            summary_week = self.json_response['daily']['summary']
            self.forecast_response = 'It is %s and %d degrees, feeling like %d. Expect %s' % (summary_now, temp_current, temp_feelslike, summary_week)
        else:
            temp_min = self.json_response['daily']['data'][when]['temperatureMin']
            temp_max = self.json_response['daily']['data'][when]['temperatureMax']
            summary = self.json_response['daily']['data'][when]['summary']
            self.forecast_response = 'will see %s  With temperatures from %d to %d degrees' % (summary, temp_min, temp_max)


        if (self.json_response.get('alerts') is not None):
            print('ALERT ALERT')
            print self.json_response['alerts']

        forecast_result = self.forecast_response
        forecast_result = forecast_result.replace(u'\N{DEGREE SIGN}' + 'C',' degrees')
        forecast_result = forecast_result.replace('until', 'until the')
        forecast_result = forecast_result.replace('precipitation', 'rain')


        return forecast_result

    ###############################
    # Return the raw data forecast
    def get_raw_response(self):
        """
        Returns the raw JSON data from the forecast
        """

        return self.raw_response


