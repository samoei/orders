# Sendy orders combination task #

This Engineering test has been solved by using Python 3.4.3

This solution is self executable meaning it has a main method with some sample orders hence can be run as a module in python

The Code is heavily commented so as to provide better understanding when someone else is going through it.



### Steps to run the solution ###

* Clone this repo `git clone https://github.com/samoei/orders.git`
* Change directory to orders by `cd orders`
* Run `python orders.py` to view the solution

### Sample Output ###

========== COMBINATION OPPORTUNITY FOUND ==============

order 1 can be combined with order 2

order 1 distance is 271.5 which costs KES 8144.92

order 2 distance is 259.92 which costs KES 7797.45

If order 1 and order 2 is combined the cost will be 7801.37

Total savings is 8141.0

========== COMBINATION OPPORTUNITY FOUND ==============

order 4 can be combined with order 5

order 4 distance is 89.77 which costs KES 2693.09

order 5 distance is 89.65 which costs KES 2689.48

If order 4 and order 5 is combined the cost will be 2689.48

Total savings is 2693.09


[Finished in 38.7s]

### Please note the following ###
* This solution is solved by using python 3 so ensure you are testing this code from a python 3 environment
* This solution comes with sample orders in form of a list(array) of dictionaries (map). To get the best of this solution try tweaking the `placementTime`,`pickupAdd`,or `dropoffAdd`
* Remember the `pickupAdd` and `dropoffAdd` should be real addresses so that their geo locations can be retrieved. For ease just use major Kenyan towns 

### Future Improvement Opportunities ###
* This solutions takes sometime to run because of a bootleneck when getting geo location of the addresses. The geo location features should be attached to the order when its being registred and not when possible combinatons are being searched for.
* Some naive assumptations have been made especially when calculating the total savings after a possible combination has been discovered 
