from rest_framework import serializers
from .models import *


# We are using Model serializers here to serialize the models
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_name', 'email')
        # These are the fields (properties) of the user model we want to send to the front end from the back end
        # User name of course we will display publically, but email we will mainly use for identification purposes


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('address1', 'address2', 'zip_code', 'city', 'state', 'lat', 'long')
        # Represents each property of the Address model in the form of a JSON


class ApartmentSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)  # Turn the apartment address into a JSON form

    class Meta:
        model = Apartment
        fields = ('id', 'apartment_slug', 'apartment_name', 'address', 'min_cost', 'max_cost', 'website_url', 'img_url', 'overall_rating', 'review_count')


class ImportantBuildingSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)  # Put the Address in JSON form

    class Meta:
        model = ImportantBuilding
        fields = ('id', 'building_slug', 'building_name', 'address')


class UniversitySerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    # Serialize the address in a JSON form, so that with the university, the address is also displayed

    # apartments = ApartmentSerializer(read_only=True, many=True)
    important_buildings = ImportantBuildingSerializer(read_only=True, many=True)
    # Commenting these out in order to speed up processing on Front End and Back End (as one university can have many apartments and important buildings)

    print("hello")

    class Meta:
        model = University
        fields = ('id', 'university_slug', 'name', 'address', 'important_buildings', 'website_url', 'img_url')


class ReviewSerializer(serializers.ModelSerializer):
    apartment = ApartmentSerializer(read_only=True)
    likes = UserSerializer(read_only=True, many=True)
    dislikes = UserSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ApartmentReview
        fields = (
            'id', 'user', 'overall_rating', 'review_text', 'cost_rating', 'maintainence_rating', 'quietness_rating',
            'cleanliness_rating', 'apartment', 'created_at', 'updated_at', 'likes', 'dislikes')


class ApartmentSubleaseSerializer(serializers.ModelSerializer):
    associated_apartment = ApartmentSerializer(read_only=True)
    tenant = UserSerializer(read_only=True)

    class Meta:
        model = ApartmentSublease
        fields = ('id', 'associated_apartment','sublease_text','tenant', 'price', 'beds','baths')
