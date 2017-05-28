import datetime
import time
import itertools
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from geopy.exc import GeocoderTimedOut

cost = 30

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


def orders_place_recently(orders):
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
			print("If {} and {} is combined the cost will be {}".format(order1['orderName'], order2['orderName'], final_cost))
			print("Total savings is {}".format(round(total_savings, 2)))
			print("")


def can_be_picked_same_time(order1, order2):
	time = difference_in_placement_time(order1, order2)
	dist = difference_in_pickup_distance(order1, order2)
	if time < 60.0 and dist < 50.0:
		return True
	else:
		return False


def can_be_delivered_same_time(order1, order2):
	dist = difference_in_dropoff_distance(order1, order2)
	if dist < 100.0:
		return True
	else:
		return False


def difference_in_placement_time(order1, order2):
	if (order1['placementTime'] - order2['placementTime']).days < 0:
		return (order2['placementTime'] - order1['placementTime']).total_seconds() / 60
	else:
		return (order1['placementTime'] - order2['placementTime']).total_seconds() / 60


def geocode(city, recursion=0):
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
	return vincenty(location1_coord, location2_coord).km


def difference_in_pickup_distance(order1, order2):
	location1 = geocode(order1['pickupAdd'],)
	location2 = geocode(order2['pickupAdd'],)
	location1_coord = (location1.latitude, location1.longitude)
	location2_coord = (location2.latitude, location2.longitude)
	order1['pickupCoord'] = location1_coord
	order2['pickupCoord'] = location2_coord
	return distance_between_coordinates(location1_coord, location2_coord)


def difference_in_dropoff_distance(order1, order2):
	location1 = geocode(order1['dropoffAdd'])
	location2 = geocode(order2['dropoffAdd'])
	location1_coord = (location1.latitude, location1.longitude)
	location2_coord = (location2.latitude, location2.longitude)
	order1['dropoffCoord'] = location1_coord
	order2['dropoffCoord'] = location2_coord
	return distance_between_coordinates(location1_coord, location2_coord)


if __name__ == '__main__':
	orders_place_recently(orders)
