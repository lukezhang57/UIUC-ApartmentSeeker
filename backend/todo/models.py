import geopy.exc
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from slugify import slugify
from django import forms
from geopy.geocoders import Nominatim
from geopy.distance import geodesic, great_circle
import numpy as np
from django.contrib.auth.hashers import *
import ssl
from haversine import haversine, Unit
import openrouteservice
import requests
from datetime import *
import sys
import environ
import time


env = environ.Env()
environ.Env.read_env()

geolocator = Nominatim(user_agent="ApartmentSeeker")

def calculate_transit_time(src, dest):
  """
  This takes two coordinate pairs and calculates the average time between the two coordinates via public transport


  :param src (tuple of two) -- Latitude and longitude points of the source location
  :param dest (tuple of two) -- Latitude and longitude points of the destination location
  :return average travel time via public transport in minutes
  """
  here_api_key = env("HERE_API_KEY")
  travel_times = []
  today = date.today()

  # From today, check the transit times for the past seven days from today 
  # (Assuming that public transport operates on a weekly schedule (patterns repeat per week)) 
  for j in range(7):
    # Go to the jth day before today
    dt = today - timedelta(days=j)
    for i in range(24):
        # Check transit times at hour i at the jth day before today
        depart_time = dt.strftime("%Y-%m-%d") + "T{0}:00:00".format(i)
        data = requests.get("https://transit.router.hereapi.com/v8/routes", 
                        params={"origin":"{0},{1}".format(src[0], src[1]), "destination":"{0},{1}".format(dest[0],dest[1]), "apiKey":here_api_key, "departureTime":depart_time, "alternatives":5}).json()
        print(data)
        if 'error' in data.keys():
          # If rate limited, then approximate with GeoAPIfy (HERE API is more accurate, but GeoAPIfy gets optimized route)
          geo_apifyurl = "https://api.geoapify.com/v1/routing"
          querystring = {"waypoints": "{0},{1}|{2},{3}".format(src[0], src[1],dest[0],dest[1]), "mode": "approximated_transit", "apiKey": env("GEOAPIFY_API_KEY")}
          response = requests.request("GET", geo_apifyurl, params=querystring)
          data = response.json()
          route_total_minutes = data["features"][0]["properties"]["time"] / 60  
          return route_total_minutes
        if 'routes' in data.keys() and len(data['routes']) > 0:
            for route in data['routes']:
                if 'sections' in route.keys():
                    departure_time = datetime.strptime(data['routes'][0]['sections'][0]['departure']['time'][0:-6], "%Y-%m-%dT%H:%M:%S")
                    arrival_time = datetime.strptime(data['routes'][0]['sections'][-1]['arrival']['time'][0:-6], "%Y-%m-%dT%H:%M:%S")
                    travel_time = arrival_time - departure_time
                    minutes = travel_time.total_seconds() / 60
                    travel_times.append(minutes)

        data = requests.get("https://transit.router.hereapi.com/v8/routes", 
                        params={"origin":"{0},{1}".format(dest[0],dest[1]), "destination":"{0},{1}".format(src[0], src[1]), "apiKey":here_api_key, "departureTime":depart_time, "alternatives":5}).json()
        if 'routes' in data.keys() and len(data['routes']) > 0:
            for route in data['routes']:
                if 'sections' in route.keys():
                    departure_time = datetime.strptime(data['routes'][0]['sections'][0]['departure']['time'][0:-6], "%Y-%m-%dT%H:%M:%S")
                    arrival_time = datetime.strptime(data['routes'][0]['sections'][-1]['arrival']['time'][0:-6], "%Y-%m-%dT%H:%M:%S")
                    travel_time = arrival_time - departure_time
                    minutes = travel_time.total_seconds() / 60
                    travel_times.append(minutes)
    time.sleep(10)
  return np.average(np.array(travel_times)[~np.isnan(travel_times)])


# Used for getting the coordinate points and the distance calculations

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    user_name = models.SlugField(max_length=120, null=True, blank=True, unique=True)
    # Each user will have a unique username, just like Twitter and Instagram
    email = models.CharField(max_length=120, null=True, blank=True, unique=True)
    profile_photo = models.ImageField(null=True, blank=True)
    password = models.CharField(max_length=128, blank=False, null=True)

    def __str__(self):
        """
        This takes the first name, last name, and user name of the User Model and converts it into
        a displayable string format (Makes it easier on Admin side)
        :return: String form of the user containing the first and last name along with the user name
        """
        name_str = ""
        if self.first_name:
            name_str += self.first_name
        name_str += " "
        if self.last_name:
            name_str += self.last_name
        name_str += " "
        if self.user_name:
            name_str += "(" + self.user_name + ")"
        return name_str

    def generate_password(self, raw_password):
        """
        Given a password in plain text, this function generates a password hash using the 'make_password' function
        from Django's hashing library
        """
        self.password = make_password(raw_password)

    def verify_password(self, raw_password):
        """
        Helper function that uses Djangos 'check_password' function, which takes an inputted password in plain-text 
        and checks it against the hashed password stored in the 'password' field for a User.
        """
        if is_password_usable(self.password):  # checks if a user's password isn't empty and corresponds to a valid hash
            return check_password(raw_password, self.password)
        else:
            return False


class Address(models.Model):
    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024, blank=True
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    state = models.CharField("State", max_length=2, default="IL")

    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        """
        This takes the first two lines of the address (Along with the city, state, and zip code) and converts it into a displayable format
        (Makes it easier on Admin side)
        :return: The Address in string form
        """
        address_str = ""
        if self.address1:
            address_str += self.address1 + "\n"
        if self.address2:
            address_str += self.address2 + "\n"
        if self.city and self.state and self.zip_code:
            address_str += self.city + ", " + self.state + " " + self.zip_code
        return address_str

    def dist(self, another_addr):
        """
        This takes another address and computes the distance between the two addresses.
        Used for finding nearest apartments near a building
        :param another_addr: The address that we are trying to compute the distance away from
        :return: the haversine distance between the two addresses
        """
        try:
            add1 = (float(self.lat.to_decimal()), float(self.long.to_decimal()))
            add2 = (float(another_addr.lat.to_decimal()), float(another_addr.long.to_decimal()))
        except AttributeError:
            add1 = (float(self.lat), float(self.long))
            add2 = (float(another_addr.lat), float(another_addr.long))
        try:
            return haversine(add1, add2, unit=Unit.MILES)
            # Calculate distance between two points with haversine.
            # Originally used Geopy to calculate distance but currently having SSL certificate errors at the moment.
        except ValueError:
            return np.nan

    def get_walking_dist(self, another_addr):
        """
        This takes another address and computes the walking distance between the two addresses.
        Used for finding nearest apartments from a building
        :param another_addr: The address that we are trying to compute the distance away from
        :return: The walking distance between two addresses
        """
        client = openrouteservice.Client(key='5b3ce3597851110001cf62482a4d26fe8bd64a11a5a0e870521fc55e') 
        # client = openrouteservice.Client(key='5b3ce3597851110001cf62483c9e20a2f1bc45f59080565204121e2c') 
        try:
            add1 = (float(self.long.to_decimal()),float(self.lat.to_decimal()))
            add2 = (float(another_addr.long.to_decimal()),float(another_addr.lat.to_decimal()))
        except AttributeError:
            add1 = (float(self.long), float(self.lat))
            add2 = (float(another_addr.long), float(another_addr.lat))
        coords = (add1,add2)
        walking_directions = None
        try:
            walking_directions = client.directions(coords, units="mi", profile='foot-walking')
        except openrouteservice.exceptions.ApiError:
            client = openrouteservice.Client(key='5b3ce3597851110001cf62483c9e20a2f1bc45f59080565204121e2c')
            walking_directions = client.directions(coords, units="mi", profile='foot-walking')
        try:
            distance = walking_directions['routes'][0]['summary']['distance']
            return distance
            # Calculate distance between two points with haversine.
            # Originally used Geopy to calculate distance but currently having SSL certificate errors at the moment.
        except ValueError:
            return np.nan
        except KeyError:
            return 0

    def get_biking_dist(self, another_addr):
        """
        This takes another address and computes the biking distance between the two addresses.
        Used for finding nearest apartments near a building
        :param another_addr: The address that we are trying to compute the distance away from
        :return: The biking distance between two addresses
        """
        client = openrouteservice.Client(key='5b3ce3597851110001cf62482a4d26fe8bd64a11a5a0e870521fc55e') 
        # client = openrouteservice.Client(key='5b3ce3597851110001cf62483c9e20a2f1bc45f59080565204121e2c')
        try:
            add1 = (float(self.long.to_decimal()),float(self.lat.to_decimal()))
            add2 = (float(another_addr.long.to_decimal()),float(another_addr.lat.to_decimal()))
        except AttributeError:
            add1 = (float(self.long), float(self.lat))
            add2 = (float(another_addr.long), float(another_addr.lat))
        coords = (add1,add2)
        biking_directions = None
        try:
            biking_directions = client.directions(coords, units="mi", profile='cycling-regular')
        except openrouteservice.exceptions.ApiError:
            # This typically means the API quota has exceeded, so we try another API key
            client = openrouteservice.Client(key='5b3ce3597851110001cf62483c9e20a2f1bc45f59080565204121e2c')
            biking_directions = client.directions(coords, units="mi", profile='cycling-regular')
        try:
            distance = biking_directions['routes'][0]['summary']['distance']
            return distance
            # Calculate distance between two points with haversine.
            # Originally used Geopy to calculate distance but currently having SSL certificate errors at the moment.
        except ValueError:
            return np.nan
        except KeyError:
            return 0

    def get_driving_dist(self, another_addr):
        """
        This takes another address and computes the driving distance between the two addresses.
        Used for finding nearest apartments near a building
        :param another_addr: The address that we are trying to compute the distance away from
        :return: The driving distance between two addresses
        """
        client = openrouteservice.Client(key='5b3ce3597851110001cf62482a4d26fe8bd64a11a5a0e870521fc55e') 
        # client = openrouteservice.Client(key='5b3ce3597851110001cf62483c9e20a2f1bc45f59080565204121e2c') 
        try:
            add1 = (float(self.long.to_decimal()),float(self.lat.to_decimal()))
            add2 = (float(another_addr.long.to_decimal()),float(another_addr.lat.to_decimal()))
        except AttributeError:
            add1 = (float(self.long), float(self.lat))
            add2 = (float(another_addr.long), float(another_addr.lat))
        coords = (add1,add2)
        driving_directions = None
        try:
            driving_directions = client.directions(coords, units="mi", profile='driving-car')
        except openrouteservice.exceptions.ApiError:
            # This typically means the API quota has exceeded, so we try another API key
            client = openrouteservice.Client(key='5b3ce3597851110001cf62483c9e20a2f1bc45f59080565204121e2c')
            driving_directions = client.directions(coords, units="mi", profile='driving-car')
        try:
            distance = driving_directions['routes'][0]['summary']['distance']
            return distance
            # Calculate distance between two points with haversine.
            # Originally used Geopy to calculate distance but currently having SSL certificate errors at the moment.
        except ValueError:
            return np.nan
        except KeyError:
            return 0

    def get_min_transit_time(self, another_addr):
        """
        This takes another address and computes the public transport travel time between the two addresses.
        Used for finding nearest apartments near a building
        :param another_addr: The address that we are trying to compute the distance away from
        :return: The driving distance between two addresses
        """
        try:
            add1 = (float(self.lat.to_decimal()), float(self.long.to_decimal()))
            add2 = (float(another_addr.lat.to_decimal()), float(another_addr.long.to_decimal()))
        except AttributeError:
            add1 = (float(self.lat), float(self.long))
            add2 = (float(another_addr.lat), float(another_addr.long))
        try:
            return calculate_transit_time(add1, add2)
        except ValueError:
            return np.nan
        except KeyError:
            return 0

    # NOTE: Djongo causes some issues for nor indicating fields as null (hence why long and lat have null=true)

    def save(self, *args, **kwargs):
        """
        After saving the address, if the longitude and latitute coordinates (either one) aren't defined,
        it will set the coordinates based on the address with geopy
        :param args:
        :param kwargs:
        :return: None
        """
        if not self.lat or not self.long:
            address_str = self.address1 + " " + self.city + ", " + self.state
            try:
                location = geolocator.geocode(address_str)
                self.lat = location.latitude
                self.long = location.longitude
            except geopy.exc.GeocoderUnavailable:
                self.lat = 0
                self.long = 0

        super().save(*args, **kwargs)


class Apartment(models.Model):
    apartment_slug = models.SlugField(max_length=120, unique=True, null=True,
                                      blank=True)  # We are using slugs here for URL purposes + easier to keep track of apartments
    apartment_name = models.CharField(max_length=120, unique=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    min_cost = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    max_cost = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    website_url = models.URLField(max_length=2048, null=True, blank=True)
    img_url = models.URLField(max_length=2048, null=True, blank=True)
    overall_rating = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    review_count = models.IntegerField(default=0)

    def __str__(self):
        """
        This takes the name of the Apartment Model and converts it into
        a displayable string format (Makes it easier on Admin side)
        :return: String form of the Apartment containing the apartment name
        """
        apartment_str = ""
        if self.apartment_name:
            apartment_str = self.apartment_name
        return apartment_str

    def update_reviews(self):
        apartment_reviews = ApartmentReview.objects.filter(apartment=self)
        self.overall_rating = 0
        self.review_count = len(apartment_reviews)
        for review in apartment_reviews:
            self.overall_rating += review.overall_rating
        if len(apartment_reviews) != 0:
            self.overall_rating /= len(apartment_reviews)

    def save(self, *args, **kwargs):
        """
        After saving the apartment, it changes the slug name to the slugified form of the apartment name
        :param args:
        :param kwargs:
        :return: None
        """
        if self.apartment_name:
            if not self.apartment_slug:
                self.apartment_slug = slugify(self.apartment_name)
                print(self.apartment_slug)

        self.update_reviews()

        super().save(*args, **kwargs)


class ImportantBuilding(models.Model):
    building_slug = models.SlugField(max_length=120, unique=True,
                                     null=True,
                                     blank=True)
    building_name = models.CharField(max_length=120, unique=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    nearby_apartments = models.ManyToManyField(Apartment, blank=True)

    def __str__(self):
        """
        This takes the name of the ImportantBuilding Model and converts it into
        a displayable string format (Makes it easier on Admin side)
        :return: String form of the Important Building containing the building name
        """
        building_str = ""
        if self.building_name:
            building_str = self.building_name
        return building_str

    def save(self, *args, **kwargs):
        """
        After saving the apartment, it changes the slug name to the slugified form of the apartment name
        :param args:
        :param kwargs:
        :return: None
        """
        if self.building_name:
            if not self.building_slug:
                self.building_slug = slugify(self.building_name)
                print(self.building_slug)

        super().save(*args, **kwargs)


class University(models.Model):
    university_slug = models.SlugField(max_length=120, unique=True,
                                       null=True,
                                       blank=True)
    name = models.CharField(max_length=120, unique=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)
    website_url = models.URLField(max_length=2048, null=True, blank=True)
    img_url = models.URLField(max_length=2048, null=True, blank=True)
    apartments = models.ManyToManyField(Apartment, blank=True)
    # Reason we would do Many to Many field here is because we can have one apartment refer to multiple universities
    # (like Harvard and MIT or UIC and UChicago or NYU and Columbia or UCLA and USC).
    important_buildings = models.ManyToManyField(ImportantBuilding, blank=True)

    # This will make it easier for students to filter their important buildings
    # For UIUC, examples of these important buildings include ARC, ECEB, Siebel, Altgeld, ISR, Target However,
    # one important building can apply to multiple universities (like Chicago Union Station for UIC and UChicago
    # students or LA Airport for UCLA and USC students)


    def save(self, *args, **kwargs):
        """
        After saving the University, it changes the slug name to the slugified form of the university name
        :param args:
        :param kwargs:
        :return: None
        """
        if self.name:
            if not self.university_slug:
                self.university_slug = slugify(self.name)
                print(self.university_slug)

        # Update the distance matrix between the university's apartments and important buildings every time a university is saved
        for building in self.important_buildings.all():
            for apartment in self.apartments.all():
                print("Apartment:", apartment.apartment_slug, "Building:", building.building_slug)
                dist_matrix, is_created = DistanceMatrixModel.objects.get_or_create(important_building=building, apartment=apartment)
                if is_created:
                    dist_matrix.save()
                    time.sleep(30) # wait 30 seconds after running save for one distance matrix
                else:
                    print("Already created")

        super().save(*args, **kwargs)

class ApartmentReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    overall_rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    review_text = models.TextField(max_length=2048, blank=True, null=True)
    cost_rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    maintainence_rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    quietness_rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    cleanliness_rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    # likes = models.IntegerField(default=0)

    # Reason we have the created at and the updated at is because we will show when the review was created (just like
    # other review sites do)


class ApartmentSublease(models.Model):
    associated_apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # One tenant can rent in more than one place
    sublease_text = models.TextField(default="")
    price = models.DecimalField(decimal_places=2, max_digits=7, default=0)
    beds = models.IntegerField(default=1)
    baths = models.IntegerField(default=1)

class DistanceMatrixModel(models.Model): 
    # unique Model that stores key information for the distance & travel times between an important building and an apartment
    important_building = models.ForeignKey(ImportantBuilding, on_delete=models.CASCADE,null=True)
    apartment =  models.ForeignKey(Apartment, on_delete=models.CASCADE,null=True) 
    straight_distance = models.DecimalField(decimal_places = 2, default = 0, max_digits=10, null=True)
    walking_distance =  models.DecimalField(decimal_places = 2,default = 0, max_digits=9,null=True)
    biking_distance = models.DecimalField(decimal_places = 2, default = 0, max_digits=9,null=True)
    driving_distance = models.DecimalField(decimal_places = 2, default = 0, max_digits=9,null=True)
    transit_travel = models.DecimalField(decimal_places = 2, default = 0, max_digits=9,null=True)

    def save(self,  *args, **kwargs):
        if self.important_building and self.apartment:
            self.straight_distance = float(self.important_building.address.dist(self.apartment.address))
            self.walking_distance =  float(self.important_building.address.get_walking_dist(self.apartment.address))
            self.biking_distance = float(self.important_building.address.get_biking_dist(self.apartment.address))
            self.driving_distance = float(self.important_building.address.get_driving_dist(self.apartment.address))
            self.transit_travel = float(self.important_building.address.get_min_transit_time(self.apartment.address))
        super().save(*args, **kwargs)
    