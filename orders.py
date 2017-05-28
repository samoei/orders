import datetime
import time
import itertools
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.exc import GeocoderTimedOut

cost = 30
hour = 60.0  # two Orders placed in a variance of less than 60 mins, used to determine if same rider can pick these orders
max_pickup_distance_apart = 50.0  # maximum distance between two orders pick up points, used to determine if same rider can pick these orders
max_dropoff_distance_apart = 100.00  # maximum distance between two orders drop off points, used to determine if same rider can deliver these orders

orders = [
	{
		'orderName': 'order 1',
		'placementTime': datetime.datetime(2017, 5, 28, 10, 30),
		'pickupAdd': 'Mombasa Road, Nairobi Kenya',
		'dropoffAdd': 'Uganda Road Eldoret Kenya'
	},
	{
		'orderName': 'order 2',
		'placementTime': datetime.datetime(2017, 5, 28, 10, 40),
		'pickupAdd': 'Imara Daima, Nairobi Kenya',
		'dropoffAdd': 'Kapsabet'
	},
	{
		'orderName': 'order 3',
		'placementTime': datetime.datetime(2017, 5, 28, 10, 30),
		'pickupAdd': 'Nyeri',
		'dropoffAdd': 'Nairobi'
	},
	{
		'orderName': 'order 4',
		'placementTime': datetime.datetime(2017, 5, 28, 10, 30),
		'pickupAdd': 'Kisumu',
		'dropoffAdd': 'Eldoret'
	},
	{
		'orderName': 'order 5',
		'placementTime': datetime.datetime(2017, 5, 28, 10, 45),
		'pickupAdd': 'Kisumu',
		'dropoffAdd': 'Uganda Road Eldoret Kenya'
	},

]


def check_for_combination_opportunities(orders):
	""" Gets (incase of any) combination opportunities from the orders list passed """
	for order1, order2 in itertools.combinations(orders, 2):
		if can_be_picked_same_time(order1, order2) and can_be_delivered_same_time(order1, order2):
			print("========== COMBINATION OPPORTUNITY FOUND ==============")
			print("")
			print("{} can be combined with {}".format(order1['orderName'], order2['orderName']))
			order1_dist = distance_between_coordinates(order1['pickupCoord'], order1['dropoffCoord'])
			order1_cost = round(order1_dist * cost,2)
			order2_dist = distance_between_coordinates(order2['pickupCoord'], order2['dropoffCoord'])
			order2_cost = round(order2_dist * cost,2)
			dist_comb =   distance_between_coordinates(order1['pickupCoord'], order2['dropoffCoord'])
			final_cost = round(dist_comb * cost,2)
			total_savings = (order1_cost + order2_cost) - final_cost

			print ("{} distance is {} which costs KES {}".format(order1['orderName'], round(order1_dist, 2), round(order1_dist*cost, 2)))
			print ("{} distance is {} which costs KES {}".format(order2['orderName'], round(order2_dist, 2), round(order2_dist*cost, 2)))
			print("If {} and {} are combined the cost will be {}".format(order1['orderName'], order2['orderName'], final_cost))
			print("Total savings is {}".format(round(total_savings, 2)))
			print("")


def can_be_picked_same_time(order1, order2):
	"""
	Checks whether two orders can be collected by the same rider from their pick up points
	Uses time to compare the order placements of the two orders
	Uses distance between the two pickup points for comparison

	"""
	time = difference_in_placement_time(order1, order2)
	dist = difference_in_pickup_distance(order1, order2)
	if time < hour and dist < max_pickup_distance_apart:
		return True
	else:
		return False


def can_be_delivered_same_time(order1, order2):
	"""
	Checks whether two orders can be delivered by the same rider to their drop off points
	Uses distance between the two drop off points for comparison

	"""
	dist = difference_in_dropoff_distance(order1, order2)
	if dist < max_dropoff_distance_apart:
		return True
	else:
		return False


def difference_in_placement_time(order1, order2):
	"""
	Returns difference in minutes between when the two orders were placed

	"""
	if (order1['placementTime'] - order2['placementTime']).days < 0:
		return (order2['placementTime'] - order1['placementTime']).total_seconds() / 60
	else:
		return (order1['placementTime'] - order2['placementTime']).total_seconds() / 60


def geocode(city, recursion=0):
	"""
	Given a address as a string it returns a geo location for that address

	"""
	geolocator = Nominatim()
	try:
		return geolocator.geocode(city, timeout=10)
	except GeocoderTimedOut as e:
		if recursion > 10:      # max recursions
			raise e
			print("Error: geocode failed on input %s with message %s"%(city, e.message))
		time.sleep(1)  # wait a bit
		# try again
		return geocode(city, recursion=recursion + 1)


def distance_between_coordinates(location1_coord, location2_coord):
	"""
	Calculates the distance between two geo cordinates in Kilometres using Vincenty's formulae

	"""
	return vincenty(location1_coord, location2_coord).km


def difference_in_pickup_distance(order1, order2):
	"""
	Calculates the distance between two pickup points

	"""
	location1 = geocode(order1['pickupAdd'],)
	location2 = geocode(order2['pickupAdd'],)
	location1_coord = (location1.latitude, location1.longitude)
	location2_coord = (location2.latitude, location2.longitude)
	order1['pickupCoord'] = location1_coord
	order2['pickupCoord'] = location2_coord
	return distance_between_coordinates(location1_coord, location2_coord)


def difference_in_dropoff_distance(order1, order2):
	"""
	Calculates the distance between two drop off points

	"""
	location1 = geocode(order1['dropoffAdd'])
	location2 = geocode(order2['dropoffAdd'])
	location1_coord = (location1.latitude, location1.longitude)
	location2_coord = (location2.latitude, location2.longitude)
	order1['dropoffCoord'] = location1_coord
	order2['dropoffCoord'] = location2_coord
	return distance_between_coordinates(location1_coord, location2_coord)


if __name__ == '__main__':
	check_for_combination_opportunities(orders)
