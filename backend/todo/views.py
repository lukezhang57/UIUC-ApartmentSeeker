import decimal
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .serializers import *
from .models import *
import json
from django.core.mail import send_mail
from decimal import Decimal
from bson.decimal128 import Decimal128
from django.db.models import Q


# Create your views here.
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UniversityView(viewsets.ModelViewSet):
    serializer_class = UniversitySerializer
    queryset = University.objects.all()


class ApartmentView(viewsets.ModelViewSet):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()


class ReviewView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = ApartmentReview.objects.all()


class ApartmentSubleaseView(viewsets.ModelViewSet):
    serializer_class = ApartmentSubleaseSerializer
    queryset = ApartmentSublease.objects.all()


@api_view(['POST'])
def post_review(request):
    """
    This takes the request and gets the review information (review text, ratings)
    along with the apartment slug for the apartment the review is for and the user id for the user who posted/will post this,
    and then posts or updates that review for that apartment

    Preferably, this method is better for us than just using the Django model view POST request as here, we are only
    taking the use of a user and apartment identifier rather than a whole apartment (making it easier on the front
    end side as then they only have to send us the apartment slug and the user name) :param request: The HTTP request
    containing the review data, apartment slug, and user identifier in the query parameters :return: The JSON Review
    object of the review we created
    """
    try:
        # review_data = request.query_params["reviewData"]
        # This is a JSON object containing data of the review we are posting
        user_name = request.query_params["userName"]  # Used user name for testing purposes
        apartment_slug = request.query_params["apartmentSlug"]
        # Putting the query params under the try catch just for the sake of accounting for edge cases
        # review_data_dict = json.loads(review_data)
        # review_image =
        user = User.objects.get(user_name=user_name)
        apartment = Apartment.objects.get(apartment_slug=apartment_slug)
        review_text = request.query_params["reviewText"]
        review, created = ApartmentReview.objects.get_or_create(user=user,
                                                                apartment=apartment)  # If review exists, then get that
        # review as users don't (shouldn't) really put more than one review for one apartment. Also, the get_or_create
        # method returns a tuple containing the object and a boolean indicating that it was created, Hence,
        # we did "review, created = Review.objects.get_or_create(user=user, apartment=apartment)" to separate the model
        # from the tuple
        review.review_text = (
                    user.first_name + " " + user.last_name + "(" + user.user_name + "): " + review_text + "(" + apartment_slug + ")")
        # Added these checks for personalization + originally, the review text was set to unique, which caused issues
        # to the MongoDB database as then the review text was marked as unique and didn't allow duplicates
        # Causing problems, even after migrations
        review.overall_rating = request.query_params["overallRating"]
        review.cost_rating = request.query_params["costRating"]
        review.maintainence_rating = request.query_params["maintainenceRating"]
        review.quietness_rating = request.query_params["quietnessRating"]
        review.cleanliness_rating = request.query_params["cleanlinessRating"]
        # JSON Review Data query param is supposed to be in camel case
        review.save()
        if not isinstance(apartment.min_cost, decimal.Decimal):
            apartment.min_cost = apartment.min_cost.to_decimal()
            apartment.max_cost = apartment.max_cost.to_decimal()
        # These two checks are here because min_cost and max_cost is set as Decimal128 for MongoDB and Django cannot
        # parse Decimal128 well
        apartment.save()
        review_json = ReviewSerializer(review)
        return JsonResponse(review_json.data, safe=False)
    except User.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": "User does not exist"}))
    except Apartment.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": "Apartment does not exist"}))
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['POST'])
def sign_up(request):
    """
     This takes the request and gets the user information (First name, last name, user_name)
    along with the password to create a user object in order to sign up

    :param request: The data containing our query params
    :return: Data of user created (or indication of User already existing)
    """
    try:
        user_name = request.query_params["userName"]
        first_name = request.query_params["firstName"]
        last_name = request.query_params["lastName"]
        password = request.query_params["password"]
        email = request.query_params["email"]
        if not User.objects.filter(user_name=user_name).exists():
            user = User.objects.create(user_name=user_name, email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.generate_password(password)
            user.save()
            user_json = UserSerializer(user)
            return JsonResponse(user_json.data, safe=False)
        return HttpResponseBadRequest("User already exists")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['GET'])
def sign_in(request):
    """

    This takes the request and gets the user name
    along with the password in order to sign in

    :param request: The data containing our query params
    :return: Data of user we got
    """
    try:
        user_name = request.query_params["userName"]
        password = request.query_params["password"]
        try:
            user = User.objects.get(user_name=user_name)
            if user.verify_password(password):
                print("User is correct")
                user_json = UserSerializer(user)
                return JsonResponse(user_json.data, safe=False)
            else:
                return HttpResponseBadRequest("User Authentication Failure. Password is incorrect")
        except User.DoesNotExist:
            return HttpResponseBadRequest("User Authentication Failure. User does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['GET'])
def get_nearest_apartments(request):
    """
    This takes in the locations of the buildings that the user wants to live near, and finds the apartments closest to those buildings
    :param request:
    :return: Returns list of apartments close to location
    """
    building_slugs = json.loads(request.query_params["buildingSlugs"])
    university = University.objects.get(university_slug=request.query_params["universitySlug"])
    print(building_slugs)
    
    associated_buildings = []
    for slug in building_slugs:
        associated_buildings.append(ImportantBuilding.objects.get(building_slug=slug))
    print(associated_buildings)
    min_walking_dist = request.query_params.get("minWalkingDist")
    min_walking_dist = float(min_walking_dist) if min_walking_dist else -1

    min_biking_dist = request.query_params.get("minBikingDist")
    min_biking_dist = float(min_biking_dist) if min_biking_dist else -1

    min_driving_dist = request.query_params.get("minDrivingDist")
    min_driving_dist = float(min_driving_dist) if min_driving_dist else -1

    max_transit_time = request.query_params.get("maxTransitTime")
    max_transit_time = float(max_transit_time) if max_transit_time else -1
    
    all_dists_from_buildings = DistanceMatrixModel.objects.filter(important_building__in=associated_buildings)

    apartments = set()
    excluded_apartments = set()
    for dist in all_dists_from_buildings:
        # Original data type is Decimal128, so they have to convert it
        try:
            if (float(dist.walking_distance.to_decimal()) <= min_walking_dist) or float(dist.biking_distance.to_decimal()) <= min_biking_dist or float(dist.driving_distance.to_decimal()) <= min_driving_dist or float(dist.transit_travel.to_decimal()) <= max_transit_time:
                apartments.add(dist.apartment)
            else:
                # One apartment that may be near one building may not be near another
                excluded_apartments.add(dist.apartment)
        except AttributeError:
            if (float(dist.walking_distance) <= min_walking_dist) or float(dist.biking_distance) <= min_biking_dist or float(dist.driving_distance) <= min_driving_dist or float(dist.transit_travel) <= max_transit_time:
                apartments.add(dist.apartment)
            else:
                # One apartment that may be near one building may not be near another
                excluded_apartments.add(dist.apartment)

    apartments = apartments - excluded_apartments # Discard the apartments that don't fall in these requirements
    print(apartments)

    starting_index = max(0, min(int(request.query_params["starting_index"]), len(apartments)))
    # Adding starting index and ending index to speed up runtime on front end side
    ending_index = min(int(request.query_params["ending_index"]), len(apartments))
    apartments = list(apartments)[starting_index:ending_index]  # Cannot splice a set, so we splice a list
    serializer = ApartmentSerializer(apartments, many=True)
    print(serializer.data)
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def add_apartments(request):
    """
    Takes a list of apartments and apartment properties (along with properties of addresses)
    (Assuming lists are same lengths) and populate the apartments to the database
    :param request:
    :return: Indication of whether apartment adding was successful or not
    """
    try:
        university_slug = request.query_params["university_slug"]
        # Reason we are using json.loads is because some of the data we will send will be lists (which will be sent as
        # json strings), hence why we will parse them
        names = json.loads(request.query_params["names"])
        urls = json.loads(request.query_params["urls"])
        img_urls = json.loads(request.query_params["img_urls"])
        address_line_1 = json.loads(request.query_params["address_line_1"])
        zip_codes = json.loads(request.query_params["zip_codes"])
        cities = json.loads(request.query_params["cities"])
        states = json.loads(request.query_params["states"])
        min_costs = json.loads(request.query_params["min_costs"])
        max_costs = json.loads(request.query_params["max_costs"])
        lat = json.loads(request.query_params["lat"])
        long = json.loads(request.query_params["long"])

        university = University.objects.get(university_slug=university_slug)
        for i in range(len(names)):
            print(names[i])
            apartment, created = Apartment.objects.get_or_create(apartment_slug=slugify(names[i]))
            if created:
                address = Address.objects.create(address1=address_line_1[i], zip_code=zip_codes[i], city=cities[i],
                                                 lat=float(lat[i]), long=float(long[i]))
                address.state = states[i]
                address.lat = float(lat[i])
                address.long = float(long[i])
                address.save()

                apartment.address = address
            else:
                apartment.address.state = states[i]
                apartment.address.lat = float(lat[i])
                apartment.address.long = float(long[i])
                apartment.address.save()

            apartment.apartment_name = names[i]
            print(apartment.apartment_name)
            apartment.min_cost = float(min_costs[i])
            apartment.max_cost = float(max_costs[i])
            apartment.website_url = urls[i]
            apartment.img_url = img_urls[i]
            apartment.save()
            if created:
                university.apartments.add(apartment)
        university.save()
    except University.DoesNotExist:
        return HttpResponseBadRequest("University does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")
    except IndexError:
        return HttpResponseBadRequest("Not all data is the same size")

    return HttpResponse("Apartments successfully added")


@api_view(['GET'])
def get_university_apartments(request):
    """
    This takes a university slug and returns the apartments corresponding to the university
    (This is intended to help speed up the code a little as we will be dealing with multiple apartments and multiple universities)
    :param request:
    :return: The JSON request of the university apartments (or an indication that the university does not exist)
    """
    try:
        university_slug = request.query_params["university_slug"]
        starting_index = max(0,
                             int(request.query_params["starting_index"]))  # Adding starting index and ending index to
        # give bounds to which university apartments to get
        university = University.objects.get(university_slug=university_slug)
        ending_index = min(int(request.query_params["ending_index"]), len(university.apartments.all()))
        apartments = university.apartments.all()[starting_index:ending_index]
        serializer = ApartmentSerializer(apartments, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
    except University.DoesNotExist:
        return HttpResponseBadRequest("University does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['GET'])
def get_apartment_reviews(request):
    """
    This takes an apartment slug and returns all the reviews of the apartment associated with the slug

    :param request:
    :return: The JSON request of the apartment reviews (or an indication that the apartment does not exist)
    """
    try:
        apartment_slug = request.query_params["apartment_slug"]
        apartment = Apartment.objects.get(apartment_slug=apartment_slug)
        apartment_reviews = ApartmentReview.objects.filter(apartment=apartment)
        serializer = ReviewSerializer(apartment_reviews, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Apartment.DoesNotExist:
        return HttpResponseBadRequest("Apartment does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['POST'])
def like_review(request):
    """
    This takes a user_name along with the user_name of the reviewer and the apartment slug,
    and then likes a review

    :param request:
    :return: A response indicating whether or not Review was successfully liked
    (otherwise returns error messages indicating whether object does not exist)
    (Returns updated list of apartment reviews)
    """
    try:
        user_name = request.query_params["user_name"]
        review_user_name = request.query_params["review_user_name"]
        apartment_slug = request.query_params["apartment_slug"]
        apartment = Apartment.objects.get(apartment_slug=apartment_slug)
        reviewer = User.objects.get(user_name=review_user_name)
        user = User.objects.get(user_name=user_name)
        review = ApartmentReview.objects.get(apartment=apartment, user=reviewer)
        if user in review.likes.all():
            review.likes.remove(user)
            # Pressing like button again is equivalent to removing a like, like in YouTube
        else:
            review.likes.add(user)
            if user in review.dislikes.all():
                review.dislikes.remove(user)  # You cannot really like or dislike a review at the same time
        apartment_reviews = ApartmentReview.objects.filter(apartment=apartment)
        serializer = ReviewSerializer(apartment_reviews, many=True)
        return JsonResponse(serializer.data, safe=False)  # Return updated list of apartment reviews after like.
    except User.DoesNotExist:
        return HttpResponseBadRequest("User does not exist")
    except Apartment.DoesNotExist:
        return HttpResponseBadRequest("Apartment does not exist")
    except ApartmentReview.DoesNotExist:
        return HttpResponseBadRequest("Review does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['POST'])
def dislike_review(request):
    """
    This takes a user_name along with the user_name of the reviewer and the apartment slug,
    and then dislikes a review

    :param request:
    :return: A response indicating whether or not Review was successfully disliked
    (otherwise returns error messages indicating whether object does not exist)
    """
    try:
        user_name = request.query_params["user_name"]
        review_user_name = request.query_params["review_user_name"]
        apartment_slug = request.query_params["apartment_slug"]
        apartment = Apartment.objects.get(apartment_slug=apartment_slug)
        reviewer = User.objects.get(user_name=review_user_name)
        user = User.objects.get(user_name=user_name)
        review = ApartmentReview.objects.get(apartment=apartment, user=reviewer)
        if user in review.dislikes.all():
            review.dislikes.remove(user)
            # Pressing dislike button again is equivalent to removing a dislike, like in YouTube
        else:
            review.dislikes.add(user)
            if user in review.likes.all():
                review.likes.remove(user)  # You cannot really like or dislike a review at the same time
        return HttpResponse("Review successfully disliked")
    except User.DoesNotExist:
        return HttpResponseBadRequest("User does not exist")
    except Apartment.DoesNotExist:
        return HttpResponseBadRequest("Apartment does not exist")
    except ApartmentReview.DoesNotExist:
        return HttpResponseBadRequest("Review does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['POST'])
def post_sublease(request):
    """
    This takes the request and gets the sublease text
    along with the apartment slug for the apartment the review is for and the user id for the user who posted/will post this,
    and then posts or updates that sublease for that apartment
    """

    try:
        sublease_text = request.query_params[
            "subleaseText"]  # This is a JSON object containing data of the review we are posting
        user_name = request.query_params["userName"]  # Used user name for testing purposes
        apartment_slug = request.query_params["apartmentSlug"]
        price = request.query_params["price"]
        beds = request.query_params["beds"]
        baths = request.query_params["baths"]
        user = User.objects.get(user_name=user_name)
        apartment = Apartment.objects.get(apartment_slug=apartment_slug)
        sublease, created = ApartmentSublease.objects.get_or_create(tenant=user, associated_apartment=apartment)
        sublease.sublease_text = sublease_text
        sublease.price = price
        sublease.beds = beds
        sublease.baths = baths
        sublease.save()
        sublease_json = ApartmentSubleaseSerializer(sublease)
        return JsonResponse(sublease_json.data, safe=False)
    except User.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": "User does not exist"}))
    except Apartment.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": "Apartment does not exist"}))
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['GET'])
def get_apartment_subleases(request):
    """
    This takes an apartment slug and returns all the subleases of the apartment associated with the slug

    :param request:
    :return: The JSON request of the apartment subleases (or an indication that the apartment does not exist)
    """
    try:
        apartment_slug = request.query_params["apartment_slug"]
        apartment = Apartment.objects.get(apartment_slug=apartment_slug)
        apartment_subleases = ApartmentSublease.objects.filter(associated_apartment=apartment)
        serializer = ApartmentSubleaseSerializer(apartment_subleases, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Apartment.DoesNotExist:
        return HttpResponseBadRequest("Apartment does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['GET'])
def get_university_data(request):
    """
    This takes a university slug and returns the data corresponding to the university
     (original university url requires the id and not the slug)
    :param request:
    :return: The JSON request of the university data (or an indication that the university does not exist)
    """
    try:
        university_slug = request.query_params["university_slug"]
        university = University.objects.get(university_slug=university_slug)
        serializer = UniversitySerializer(university)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False)
    except University.DoesNotExist:
        return HttpResponseBadRequest("University does not exist")
    except KeyError:
        return HttpResponseBadRequest("At least one parameter is missing")


@api_view(['POST'])
def email_tenant(request):
    """
    This takes the tenant email along with the current subtenant username to notify the tenant that the subtenant is interested in subleasing.
    This also personalizes the email message so that it tries to point out to the tenant about the subtentant's information and the apartment the sublease was posted at

    :param request:
    :return: 
    """
    try:
        tenant_username = request.query_params["tenant_username"]
        subtenant_username = request.query_params["subtenant_username"]
        email_text = request.query_params["email_text"]
        apartment_slug = request.query_params["apartment_slug"]
        apartment = Apartment.objects.get(apartment_slug=apartment_slug)
        subtenant = User.objects.get(user_name=subtenant_username)
        tenant = User.objects.get(user_name=tenant_username)
        email_subject = subtenant.first_name + " " + subtenant.last_name + "(" + subtenant.user_name + ") has messaged you regarding your sublease in " + apartment.apartment_name
        send_mail(
            email_subject,
            email_text,
            subtenant.email,
            [tenant.email],
            fail_silently=False,
        )
        return HttpResponse("Email sent successfully")
    except User.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": "User does not exist"}))
    except Apartment.DoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": "Apartment does not exist"}))
