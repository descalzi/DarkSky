#! /usr/bin/python

import DarkSky
forecast = DarkSky.DarkSky(api_key='4e1f0dca2ec3641450bebbdc2f4213af', location_lat='51.5096272', location_long='-0.087692')
forecast.get_forecast()
#print forecast.get_raw_response()
print forecast.get_pretty_summary('today')
print 'Tomorrow ' + forecast.get_pretty_summary('tomorrow')
print 'In two days ' + forecast.get_pretty_summary(2)
print 'In three days ' + forecast.get_pretty_summary(3)

