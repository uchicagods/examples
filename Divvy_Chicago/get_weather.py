import pandas as pd
import requests
from datetime import datetime
import logging


def get_weather(unit='daily'):
	
	'''
	Collects daily weather information from 1/1/18 to 12/31/18.
	Assuming that the weather does not vary much by zipcodes within Chicago.
	For convenience, collected data using lat=41.907781 , lon=-87.685854, zipcode=60622.
	'''

	# Reading unix data.
	unix_date = pd.read_csv("unix_date.csv", index_col=0)

	API_KEY = 'PUT YOUR API KEY HERE'
	info_dict = {'date':[], 'summary':[], 'sunrise':[], 'sunset':[], 'temp_high':[], 'temp_low':[],\
	'precip_intensity':[], 'precip_prob':[], 'humidity':[], 'windespeed':[], 'cloudcover':[],\
	'visibility':[]}
	errors = []


	# Getting data using the API.
	for date in unix_date['date']:

		page_link = 'https://api.darksky.net/forecast/{}/41.907781,-87.685854,{}'.format(API_KEY, date)
		convert_to_date = datetime.utcfromtimestamp(date).strftime('%Y-%m-%d')
		print("Processing: ", convert_to_date)

		try:
			weather_info = requests.get(page_link, timeout=5).json()[unit]['data'][0]
			info_dict['date'].append(convert_to_date)
			info_dict['summary'].append(weather_info['icon'])
			info_dict['sunrise'].append(weather_info['sunriseTime'])
			info_dict['sunset'].append(weather_info['sunsetTime'])
			info_dict['temp_high'].append(weather_info['temperatureHigh'])
			info_dict['temp_low'].append(weather_info['temperatureLow'])
			info_dict['precip_intensity'].append(weather_info['precipIntensity'])
			info_dict['precip_prob'].append(weather_info['precipProbability'])
			info_dict['humidity'].append(weather_info['humidity'])
			info_dict['windespeed'].append(weather_info['windSpeed'])
			info_dict['cloudcover'].append(weather_info['cloudCover'])
			info_dict['visibility'].append(weather_info['visibility'])


		except Exception as e:
			logging.exception("Exception Occurred...")
			errors.append(date)
			continue


	# Creating a dataframe by concantenating the collected data column-wise.

	data_list = []
	for column in info_dict.keys():
		data_list.append(pd.Series(info_dict[column], name=column))

	df = pd.concat(data_list, axis=1)


	# Export the dataframe to 'csv' file with specified filename.
	df.to_csv("weather_info.csv")


	return None




if __name__ == '__main__':

	get_weather()
