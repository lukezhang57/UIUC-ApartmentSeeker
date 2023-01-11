import openrouteservice

coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key='5b3ce3597851110001cf62482a4d26fe8bd64a11a5a0e870521fc55e') # Specify your personal API key
car = client.directions(coords,units="mi",profile='driving-car')
bike = client.directions(coords,units="mi",profile='cycling-regular')
walk = client.directions(coords,units="mi",profile='foot-walking')

#print(routes)
print(car['routes'][0]['summary']['distance'])
print(bike['routes'][0]['summary']['distance'])
print(walk['routes'][0]['summary']['distance'])