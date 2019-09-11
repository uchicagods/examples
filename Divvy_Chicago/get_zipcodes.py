import pandas as pd
import logging
import googlemaps



def get_zipcode(latitude='FROM LATITUDE', longitude='FROM LONGITUDE', name='from'):

	# Reading Divvy Data.
	divvy = pd.read_csv("Divvy_Trips_2018.csv")

	# Preprocessing the data by dropping duplicates of a pair of lat, lon.
	divvy = divvy.drop_duplicates(subset=[latitude, longitude])

	# Printing out the info.
	print("Data Size: ", divvy.shape)
	print("Preprocessing Done")

	"""
	Getting zipcodes with latitudes and longitudes using Google Geocoding API

	"""

	API_KEY = 'PUT API KEY HERE'
	info_dict = {'latitude':[], 'longitude':[], 'zipcode':[]}

	gmaps = googlemaps.Client(key=API_KEY)

	for (lat, lon) in zip(divvy[latitude].values, divvy[longitude].values):
		print("Processing ({},{})".format(lat, lon))

		try:
			reverse_geocode_result = gmaps.reverse_geocode(("{},{}").format(lat, lon))
			info_dict['latitude'].append(lat)
			info_dict['longitude'].append(lon)
			info_dict['zipcode'].append(reverse_geocode_result[0]['address_components'][-1]['long_name'])
			# info_dict['zipcode'].append(reverse_geocode_result[0]['formatted_address'].split(',')[2][4:])

		except Exception as e:
			logging.exception("Exception Occurred...")
			continue


	# Creating a dataframe by concantenating the collected data column-wise.
	s1 = pd.Series(info_dict['longitude'], name='longitude')
	s2 = pd.Series(info_dict['latitude'], name='latitude')
	s3 = pd.Series(info_dict['zipcode'], name='zipcode')
	df = pd.concat([s1,s2,s3], axis=1)

	# For all columns, if it's guaranteed to have the same number of data, can use below code instead.
	# df = pd.DataFrame.from_dict(info_dict)

	# Export the dataframe to 'csv' file with specified filename.
	df.to_csv("zipcode{}.csv".format(name))

	return None


if __name__ == '__main__':

	get_zipcode()
	get_zipcode('TO LATITUDE', 'TO LONGITUDE', 'to')
