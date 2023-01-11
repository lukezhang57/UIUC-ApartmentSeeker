import openrouteservice

coords = ((8.34234,48.23424),(8.34423,48.26424))

client = openrouteservice.Client(key='') # Specify your personal API key
routes = client.directions(coords)

print(routes)