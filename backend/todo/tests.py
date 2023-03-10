import json

from django.db import IntegrityError
from django.test import TestCase
from rest_framework.reverse import reverse

from todo.models import *
from decimal import Decimal
from rest_framework import status
from rest_framework.test import APITestCase
import math


# Create your tests here.
# Following documentation from: https://docs.djangoproject.com/en/4.0/topics/testing/overview/
class UserTestCase(TestCase):  # Test cases testing the user model
    def setUp(self):
        """
        This is where we set up some dummy user models for testing
        :return:
        """
        User.objects.create(first_name="Dummy", last_name="d", user_name="Dummy1", email="email@email.com")
        User.objects.create(first_name="Dummy2", last_name="D", user_name="Dummy2", email="email2@email.com")
        User.objects.create(first_name="John", last_name="Doe", user_name="john_doe", email="johndoe@gmail.com")
        User.objects.create(first_name="John", last_name="Doe", user_name="johnDoe", email="johndoe@outlook.com")

    def test_different_users(self):
        """Users that have different names and email identified"""
        dummy_one = User.objects.get(first_name="Dummy", last_name="d", user_name="Dummy1", email="email@email.com")
        dummy_two = User.objects.get(first_name="Dummy2", last_name="D", user_name="Dummy2", email="email2@email.com")
        self.assertNotEqual(dummy_one.first_name, dummy_two.first_name)
        self.assertNotEqual(dummy_one.last_name, dummy_two.last_name)
        self.assertNotEqual(dummy_one.email, dummy_two.email)

    def test_users_same_name_diff_email_and_username(self):
        "Compare users that have the same first name but not the same username and not the same email"
        john_doe_one = User.objects.get(first_name="John", last_name="Doe", user_name="john_doe",
                                        email="johndoe@gmail.com")
        john_doe_two = User.objects.get(first_name="John", last_name="Doe", user_name="johnDoe",
                                        email="johndoe@outlook.com")
        self.assertEqual(john_doe_one.first_name, john_doe_two.first_name)  # Two names are equal
        self.assertNotEqual(john_doe_one.email, john_doe_two.email)  # Emails cannot be equal
        self.assertNotEqual(john_doe_one.user_name, john_doe_two.user_name)  # User names cannot be equal

    def test_unique_username(self):
        """
        Tests for uniqueness of usernames among users
        :return: None
        """
        with self.assertRaises(IntegrityError):
            User.objects.create(first_name="John", last_name="Doe", user_name="john_doe", email="johndoe@yahoo.com")

    def test_unique_email(self):
        """
        Tests for uniqueness of emails among users
        :return: None
        """
        with self.assertRaises(IntegrityError):
            User.objects.create(first_name="Jane", last_name="Doe", user_name="jane_doe", email="johndoe@gmail.com")

    def test_password(self):
        """
        Tests two passwords for user. Asserts true for correct password while asserts false for incorrect password
        :return:
        """
        dummy_one = User.objects.get(first_name="Dummy", last_name="d", user_name="Dummy1", email="email@email.com")
        dummy_one.generate_password("password")
        dummy_one.save()
        self.assertTrue(dummy_one.verify_password("password"))
        self.assertFalse(dummy_one.verify_password("Password"))


class AddressTestCase(TestCase):
    def setUp(self) -> None:
        Address.objects.create(address1="101 E Green St", zip_code="61020", city="Champaign", lat=Decimal('0'),
                               long=Decimal('0'))
        Address.objects.create(address1="102 E Green St", zip_code="61001", city="Urbana", lat=Decimal('1'),
                               long=Decimal('0'))
        Address.objects.create(address1="309 Green St", zip_code="61020", city="Champaign", lat=Decimal('0'),
                               long=Decimal('0'))

    def test_different_addresses(self):
        """
        Checks for the two addresses being different.

        Different addresses generally have different cities, zip codes, and or address lines (mainlyu address lines)
        :return:
        """
        dummy1 = Address.objects.get(address1="101 E Green St", zip_code="61020", city="Champaign")
        dummy2 = Address.objects.get(address1="102 E Green St", zip_code="61001")
        self.assertNotEqual(dummy1.address1, dummy2.address1)
        self.assertNotEqual(dummy1.zip_code, dummy2.zip_code)
        self.assertNotEqual(dummy1.city, dummy2.city)

    def test_addresses_same_city_different_addresses(self):
        """
        You can have two addresses in the same city with the same zip code, but different address lines
        :return:
        """
        dummy1 = Address.objects.get(address1="309 Green St", city="Champaign")
        dummy2 = Address.objects.get(address1="101 E Green St", city="Champaign")
        self.assertEqual(dummy1.city, dummy2.city)
        self.assertNotEqual(dummy1.address1, dummy2.address1)
        self.assertEqual(dummy1.zip_code, dummy2.zip_code)

    def test_dist_between_two_addresses(self):
        """
        Checks for distance between two addresses, and checks if it is within the actual distance
        :return:
        """
        dummy1 = Address.objects.get(address1="309 Green St", city="Champaign")
        dummy2 = Address.objects.get(address1="102 E Green St", zip_code="61001")
        # print(dummy2.lat)
        dummy1.lat = Decimal('0.000')
        dummy1.long = Decimal('0.000')
        dummy2.lat = Decimal('1.000')
        dummy2.long = Decimal('0.000')
        distance = dummy1.dist(dummy2)
        self.assertAlmostEqual(distance, 69.09, 2)  # used a calculator to get actual haversine distance between test points
        # test up to 2 decimal places


class ApartmentTestCase(TestCase):
    def setUp(self) -> None:
        Apartment.objects.create(apartment_slug="309",
                                 apartment_name="309 Green",
                                 address=Address.objects.create(address1="309 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109880),
                                                                long=Decimal(-88.247940)),
                                 min_cost=800,
                                 max_cost=1000,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/309-green"
                                 )
        Apartment.objects.create(apartment_slug="Suites",
                                 apartment_name="The Suites at Third",
                                 address=Address.objects.create(address1="705 S 3rd St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109370),
                                                                long=Decimal(-88.235970)),
                                 min_cost=714,
                                 max_cost=899,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd"
                                 )

    def test_different_apartments(self):
        """
        Compares two different apartments by name, address, and
        :return:
        """
        dummy1 = Apartment.objects.get(apartment_slug="309", apartment_name="309 Green")
        dummy2 = Apartment.objects.get(apartment_slug="Suites", apartment_name="The Suites at Third")
        self.assertNotEqual(dummy1.apartment_name, dummy2.apartment_name)
        self.assertNotEqual(dummy1.address, dummy2.address)
        self.assertNotEqual(dummy1.min_cost, dummy2.min_cost)
        self.assertNotEqual(dummy1.max_cost, dummy2.max_cost)
        self.assertEqual(dummy1.address.city, dummy2.address.city)

    def test_reviews(self):
        apartment = Apartment.objects.get(apartment_slug="309", apartment_name="309 Green")
        dummy_user = User.objects.create(first_name="Dummy", last_name="d", user_name="Dummy1", email="email@email.com")
        review = ApartmentReview.objects.create(user=dummy_user, apartment=apartment)
        review.review_text = "Nice place to live, but very expensive and maintenance. It is also very difficult place to cope as well."
        review.save()
        self.assertEqual(review.user, dummy_user)
        self.assertEqual(review.apartment, apartment)
        self.assertEqual(len(ApartmentReview.objects.all()), 1)
        dummy_user_two = User.objects.create(first_name="Dummy2", last_name="d", user_name="Dummy2",
                                             email="email2@email.com")
        review_two = ApartmentReview.objects.create(user=dummy_user_two, apartment=apartment)
        review_two.review_text = "Nice place to live, but very expensive and maintenance. It is also very difficult place to cope as well."
        review_two.save()
        self.assertEqual(review_two.user, dummy_user_two)
        self.assertEqual(review_two.apartment, apartment)
        self.assertEqual(len(ApartmentReview.objects.all()), 2)
        self.assertEqual(review_two.review_text,
                         review.review_text)  # Two people can put the same review with the same text

        apartment_two = Apartment.objects.get(apartment_slug="Suites",
                                              apartment_name="The Suites at Third")

        review_three = ApartmentReview.objects.create(user=dummy_user, apartment=apartment_two)
        review_three.review_text = "Nice place to live, but very expensive and maintenance. It is also very difficult place to cope as well."
        review_three.save()
        self.assertEqual(review_three.user, dummy_user)
        self.assertEqual(review_three.apartment, apartment_two)
        self.assertEqual(len(ApartmentReview.objects.all()), 3)
        self.assertEqual(review_three.review_text,
                         review.review_text)  # One person can put the same review for a different apartment


class AuthenticationTest(APITestCase):
    def setUp(self):
        """
        Ensure we can create a new User object by signing up
        """
        user_name = "yugMittlees"
        first_name = "Yu"
        last_name = "Mitale"
        password = "apartmentseekers"
        email = "ymiet2@example.com"
        url = f"/api/sign_up?password={password}&userName={user_name}&firstName={first_name}&lastName={last_name}&email={email}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_create_duplicate_user(self):
        """
        This checks for a 400 status code if a user already exists (No new user created)
        :return:
        """
        user_name = "yugMittlees"
        first_name = "Yu"
        last_name = "Mitaled"
        password = "apartmentseekerss"
        email = "ymiet2@example.com"
        url = f"/api/sign_up?password={password}&userName={user_name}&firstName={first_name}&lastName={last_name}&email={email}"
        # self.client.post(url, format='json')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_sign_in(self):
        """
        This tests for signing in with the user which was just created
        :return:
        """
        user_name = "yugMittlees"
        password = "apartmentseekers"
        url = f"/api/sign_in?password={password}&userName={user_name}"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_in_incorrect_password(self):
        """
        This checks for if a user put an incorrect password when signing in.
        400 status code for incorrect password

        :return:
        """
        user_name = "yugMittlees"
        password = "apartmentSeekers"
        url = f"/api/sign_in?password={password}&userName={user_name}"
        response = self.client.get(url, format='json')
        self.assertTrue("User Authentication Failure. Password is incorrect" in str(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_nonexisting_user(self):
        """
        This checks for whether or not a user exists when signing. Checks for 400 status code for nonexisting users
        :return:
        """
        user_name = "yugMittledes"
        password = "apartmentseekers"
        url = f"/api/sign_in?password={password}&userName={user_name}"
        response = self.client.get(url, format='json')
        self.assertTrue("User Authentication Failure. User does not exist" in str(response.content))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ApartmentReviewTest(APITestCase):
    def setUp(self):
        Apartment.objects.create(apartment_slug="309",
                                 apartment_name="309 Green",
                                 address=Address.objects.create(address1="309 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109880),
                                                                long=Decimal(-88.247940)),
                                 min_cost=800,
                                 max_cost=1000,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/309-green"
                                 )
        Apartment.objects.create(apartment_slug="Suites",
                                 apartment_name="The Suites at Third",
                                 address=Address.objects.create(address1="705 S 3rd St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109370),
                                                                long=Decimal(-88.235970)),
                                 min_cost=714,
                                 max_cost=899,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd"
                                 )

        user_name = "yugMittle"
        first_name = "Yu"
        last_name = "Mitale"
        password = "apartmentseekers"
        email = "ymiet2@example.com"
        url = f"/api/sign_up?password={password}&userName={user_name}&firstName={first_name}&lastName={last_name}&email={email}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        User.objects.create(first_name="Dummy", last_name="d", user_name="Dummy1", email="email@email.com")
        review_text = "Nice place to live, but very expensive and maintenance. It is also very difficult place to cope as well."
        overall_rating = 3
        cost_rating = 2
        maintainence_rating = 2
        quietness_rating = 3
        cleanliness_rating = 4
        apartment_slug = "Suites"
        user_name = "Dummy1"
        url = f"/api/post_review?apartmentSlug={apartment_slug}&userName={user_name}&reviewText={review_text}&maintainenceRating={maintainence_rating}&overallRating={overall_rating}&cleanlinessRating={cleanliness_rating}&quietnessRating={quietness_rating}&costRating={cost_rating}"
        self.client.post(url, format='json')

    def test_post_review(self):
        """
        This checks for whether the review was successfully posted to one of the test apartment.
        It compares the created review to the parameters that were passed.

        A 200 status code and review contents matching parameters passed means function is working as expected

        :return:
        """
        review_text = "Nice place to live, but very expensive and maintenance. It is also very difficult place to cope as well."
        overall_rating = 3
        cost_rating = 2
        maintainence_rating = 2
        quietness_rating = 3
        cleanliness_rating = 4
        apartment_slug = "Suites"
        user_name = "yugMittle"
        url = f"/api/post_review?apartmentSlug={apartment_slug}&userName={user_name}&reviewText={review_text}&maintainenceRating={maintainence_rating}&overallRating={overall_rating}&cleanlinessRating={cleanliness_rating}&quietnessRating={quietness_rating}&costRating={cost_rating}"
        response = self.client.post(url, format='json')
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Review successfully posted
        self.assertEqual(ApartmentReview.objects.count(), 2)  # Adds one review (one review already in set up)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug="Suites"),
                                             user=User.objects.get(user_name=user_name))

        # Check if each of the review properties are the same as what was sent to the input
        self.assertTrue(review_text in review.review_text)
        self.assertEqual(review.overall_rating, overall_rating)
        self.assertEqual(review.cost_rating, cost_rating)
        self.assertEqual(review.maintainence_rating, maintainence_rating)
        self.assertEqual(review.cleanliness_rating, cleanliness_rating)

    def test_post_review_other_apartment(self):
        """
        This checks for whether the review was successfully posted to another of the test apartment. (one person can put reviews in another apartment)
        It compares the created review to the parameters that were passed.

        A 200 status code and review contents matching parameters passed means function is working as expected

        :return:
        """
        review_text = "Nice place to live, but very expensive and maintenance. It is also very difficult place to cope as well."
        overall_rating = 3
        cost_rating = 2
        maintainence_rating = 2
        quietness_rating = 3
        cleanliness_rating = 4
        apartment_slug = "Suites"
        user_name = "yugMittle"
        url = f"/api/post_review?apartmentSlug={apartment_slug}&userName={user_name}&reviewText={review_text}&maintainenceRating={maintainence_rating}&overallRating={overall_rating}&cleanlinessRating={cleanliness_rating}&quietnessRating={quietness_rating}&costRating={cost_rating}"
        self.client.post(url, format='json')
        apartment_slug_two = "309"
        url = f"/api/post_review?apartmentSlug={apartment_slug_two}&userName={user_name}&reviewText={review_text}&maintainenceRating={maintainence_rating}&overallRating={overall_rating}&cleanlinessRating={cleanliness_rating}&quietnessRating={quietness_rating}&costRating={cost_rating}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Review successfully posted
        self.assertEqual(ApartmentReview.objects.count(),
                         3)  # Adds two more reviews (one for one apartment and one for the other)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug="309"),
                                             user=User.objects.get(user_name=user_name))

        # Check if each of the review properties are the same (or contain) as what was sent to the input
        self.assertTrue(review_text in review.review_text)
        # self.assertEqual(review_text ,review.review_text)
        self.assertEqual(review.overall_rating, overall_rating)
        self.assertEqual(review.cost_rating, cost_rating)
        self.assertEqual(review.maintainence_rating, maintainence_rating)
        self.assertEqual(review.cleanliness_rating, cleanliness_rating)

    def test_like_review(self):
        """
        This takes the review created by the set up and has one user like it. Checks the like counter of the review after

        :return:
        """
        user_name = "yugMittle"
        reviewer_user = "Dummy1"
        apartment_slug = "Suites"
        url = f"/api/like_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        response = self.client.post(url, format='json')
        print("Like review = ", response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug=apartment_slug),
                                             user=User.objects.get(user_name=reviewer_user))
        self.assertEqual(review.likes.count(), 1)  # Check if number of likes was incremented by 1 in review

    def test_remove_like(self):
        """
        This takes the review created by the set up and has one user like it, then remove the like. Checks the like counter of the review after

        :return:
        """
        user_name = "yugMittle"
        reviewer_user = "Dummy1"
        apartment_slug = "Suites"
        url = f"/api/like_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        self.client.post(url, format='json')  # First like
        response = self.client.post(url, format='json')  # Then remove like
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug=apartment_slug),
                                             user=User.objects.get(user_name=reviewer_user))
        self.assertEqual(review.likes.count(), 0)  # Removing like means review has no likes

    def test_dislike_review(self):
        """
        This takes the review created by the set up and has one user dislike it. Checks the dislike counter of the review after

        Also check 200 status code for successful request pass

        :return:
        """
        user_name = "yugMittle"
        reviewer_user = "Dummy1"
        apartment_slug = "Suites"
        url = f"/api/dislike_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug=apartment_slug),
                                             user=User.objects.get(user_name=reviewer_user))
        self.assertEqual(review.dislikes.count(), 1)  # Dislike count incremented by 1 after dislike

    def test_remove_dislike(self):
        """
        This takes the review created by the set up and has one user dislike it, then remove the dislike. Checks the dislike counter of the review after

        Also check 200 status code for successful request pass

        :return:
        """
        user_name = "yugMittle"
        reviewer_user = "Dummy1"
        apartment_slug = "Suites"
        url = f"/api/dislike_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        self.client.post(url, format='json')  # First dislike
        response = self.client.post(url, format='json')  # Then remove dislike
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug=apartment_slug),
                                             user=User.objects.get(user_name=reviewer_user))
        self.assertEqual(review.dislikes.count(), 0)

    def test_like_then_dislike(self):
        """
        This takes the review created by the set up and has one user like it, then dislike it.
        Checks the likes and dislike counter of the review after

        Also check 200 status code for successful request pass

        Expected behavior: After user dislikes a review, if the user previously liked the review, then the dislike counter increases and the like counter increases

        :return:
        """
        user_name = "yugMittle"
        reviewer_user = "Dummy1"
        apartment_slug = "Suites"
        url = f"/api/like_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug=apartment_slug),
                                             user=User.objects.get(user_name=reviewer_user))
        self.assertEqual(review.likes.count(), 1)
        self.assertEqual(review.dislikes.count(), 0)
        url = f"/api/dislike_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(review.likes.count(), 0)
        self.assertEqual(review.dislikes.count(), 1)
        review.dislikes.clear()

    def dislike_then_like_test(self):
        """
        This takes the review created by the set up and has one user dislike it, then like it.
        Checks the likes and dislike counter of the review after

        Also check 200 status code for successful request pass

        Expected behavior: After user dislikes a review, if the user previously liked the review, then the dislike counter increases and the like counter increases

        :return:
        """
        user_name = "Dummy"
        reviewer_user = "yugMittle"
        apartment_slug = "Suites"
        url = f"/api/like_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        review = ApartmentReview.objects.get(apartment=Apartment.objects.get(apartment_slug=apartment_slug),
                                             user=User.objects.get(user_name=user_name))
        self.assertEqual(review.likes.count(), 0)
        self.assertEqual(review.dislikes.count(), 1)
        # After disliking, like count right now is 0 and dislike count is 1
        url = f"/api/dislike_review?user_name={user_name}&review_user_name={reviewer_user}&apartment_slug={apartment_slug}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(review.likes.count(), 1)
        self.assertEqual(review.dislikes.count(), 0)
        # After liking, the user's dislike is removed and the like counter increases


class SubleaseTest(APITestCase):
    def setUp(self):
        Apartment.objects.create(apartment_slug="309",
                                 apartment_name="309 Green",
                                 address=Address.objects.create(address1="309 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109880),
                                                                long=Decimal(-88.247940)),
                                 min_cost=800,
                                 max_cost=1000,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/309-green"
                                 )
        Apartment.objects.create(apartment_slug="Suites",
                                 apartment_name="The Suites at Third",
                                 address=Address.objects.create(address1="705 S 3rd St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109370),
                                                                long=Decimal(-88.235970)),
                                 min_cost=714,
                                 max_cost=899,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd"
                                 )

        user_name = "yugMittle"
        first_name = "Yu"
        last_name = "Mitale"
        password = "apartmentseekers"
        email = "ymiet2@example.com"
        url = f"/api/sign_up?password={password}&userName={user_name}&firstName={first_name}&lastName={last_name}&email={email}"
        self.client.post(url, format='json')
        User.objects.create(first_name="Dummy", last_name="d", user_name="Dummy1", email="email@email.com")

    def test_post_sublease(self):
        """
        This takes an apartment slug and user created above and has a user post a sublease to that apartment

        Checks for sublease contents matching input + 200 status code indicating success

        :return:
        """
        apartment_slug = "Suites"
        user_name = "yugMittle"
        sublease_text = "sdfdsfs"
        price = 800
        beds = 2
        baths = 2
        url = f"/api/post_sublease?apartmentSlug={apartment_slug}&userName={user_name}&subleaseText={sublease_text}&beds={beds}&baths={baths}&price={price}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Sublease successfully posted
        self.assertEqual(ApartmentSublease.objects.count(), 1)  # Adds one sublease
        sublease = ApartmentSublease.objects.get(associated_apartment=Apartment.objects.get(apartment_slug="Suites"),
                                                 tenant=User.objects.get(user_name=user_name))

        # Check sublease contents
        self.assertEqual(sublease_text, sublease.sublease_text)
        self.assertEqual(price, sublease.price)
        self.assertEqual(beds, sublease.beds)
        self.assertEqual(baths, sublease.baths)

    def test_post_sublease_other_apartment(self):
        """
        This test case checks for allowing the submission of the same sublease contents to two different apartments

        :return:
        """
        apartment_slug = "Suites"
        user_name = "yugMittle"
        sublease_text = "sdfdsfs"
        price = 800
        beds = 2
        baths = 2
        url = f"/api/post_sublease?apartmentSlug={apartment_slug}&userName={user_name}&subleaseText={sublease_text}&beds={beds}&baths={baths}&price={price}"
        self.client.post(url, format='json')
        apartment_slug = "309"
        url = f"/api/post_sublease?apartmentSlug={apartment_slug}&userName={user_name}&subleaseText={sublease_text}&beds={beds}&baths={baths}&price={price}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Sublease successfully posted
        self.assertEqual(ApartmentSublease.objects.count(), 2)  # Adds one sublease
        sublease = ApartmentSublease.objects.get(associated_apartment=Apartment.objects.get(apartment_slug="Suites"),
                                                 tenant=User.objects.get(user_name=user_name))
        sublease_two = ApartmentSublease.objects.get(associated_apartment=Apartment.objects.get(apartment_slug="309"),
                                                     tenant=User.objects.get(user_name=user_name))

        # Check for the contents of the two subleases
        # Everything should be the same except the apartments they post to
        # As user posted same sublease contents to one apartment as well as the other
        self.assertEqual(sublease.sublease_text, sublease_two.sublease_text)
        self.assertEqual(sublease.price, sublease_two.price)
        self.assertEqual(sublease.beds, sublease_two.beds)
        self.assertEqual(sublease.baths, sublease_two.baths)
        self.assertNotEqual(sublease.associated_apartment, sublease_two.associated_apartment)

    def test_post_sublease_one_apartment(self):
        """
        This takes an apartment slug and user created above and has a user post a sublease to that apartment.
        This time, it tries to post twice to one apartment, but you can only post one sublease in an apartment
        (Doesn't really make sense to rent in two apartments of the same building)

        Checks for sublease contents matching input + 200 status code indicating success

        :return:
        """
        apartment_slug = "Suites"
        user_name = "yugMittle"
        sublease_text = "sdfdsfs"
        price = 800
        beds = 2
        baths = 2
        url = f"/api/post_sublease?apartmentSlug={apartment_slug}&userName={user_name}&subleaseText={sublease_text}&beds={beds}&baths={baths}&price={price}"
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Sublease successfully posted
        self.assertEqual(ApartmentSublease.objects.count(), 1)  # Adds one sublease
        sublease = ApartmentSublease.objects.get(associated_apartment=Apartment.objects.get(apartment_slug="Suites"),
                                                 tenant=User.objects.get(user_name=user_name))

        # Check sublease contents
        self.assertEqual(sublease_text, sublease.sublease_text)
        self.assertEqual(price, sublease.price)
        self.assertEqual(beds, sublease.beds)
        self.assertEqual(baths, sublease.baths)
        apartment_slug = "Suites"
        user_name = "yugMittle"
        sublease_text = "Hello there"
        price = 400
        beds = 3
        baths = 2
        url = f"/api/post_sublease?apartmentSlug={apartment_slug}&userName={user_name}&subleaseText={sublease_text}&beds={beds}&baths={baths}&price={price}"
        response = self.client.post(url, format='json')
        sublease = ApartmentSublease.objects.get(associated_apartment=Apartment.objects.get(apartment_slug="Suites"),
                                                 tenant=User.objects.get(user_name=user_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Sublease successfully posted
        self.assertEqual(ApartmentSublease.objects.count(), 1)  # No sublease added, sublease content just changes
        self.assertEqual(sublease_text, sublease.sublease_text)
        self.assertEqual(price, sublease.price)
        self.assertEqual(beds, sublease.beds)
        self.assertEqual(baths, sublease.baths)


class NearestApartmentsTest(APITestCase):
    def setUp(self):
        Apartment.objects.create(apartment_slug="309",
                                 apartment_name="309 Green",
                                 address=Address.objects.create(address1="309 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109880),
                                                                long=Decimal(-88.247940)),
                                 min_cost=800,
                                 max_cost=1000,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/309-green"
                                 )
        Apartment.objects.create(apartment_slug="308",
                                 apartment_name="308 Green",
                                 address=Address.objects.create(address1="308 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.12),
                                                                long=Decimal(-88.247940)),
                                 min_cost=800,
                                 max_cost=1000,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/309-green"
                                 )
        Apartment.objects.create(apartment_slug="Suites",
                                 apartment_name="The Suites at Third",
                                 address=Address.objects.create(address1="705 S 3rd St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.109370),
                                                                long=Decimal(-88.235970)),
                                 min_cost=714,
                                 max_cost=899,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd"
                                 )
        Apartment.objects.create(apartment_slug="the-suite",
                                 apartment_name="The Suites",
                                 address=Address.objects.create(address1="770 S 3rd St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.2),
                                                                long=Decimal(-88.235970)),
                                 min_cost=714,
                                 max_cost=899,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd"
                                 )
        Apartment.objects.create(apartment_slug="suite-life",
                                 apartment_name="The Suites Life",
                                 address=Address.objects.create(address1="770 S 4th St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.2),
                                                                long=Decimal(-88.236)),
                                 min_cost=714,
                                 max_cost=899,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd"
                                 )

    def test_get_nearest_apartments(self):
        """
        Create two important buildings near some of the apartments and then tests the nearest apartments to the buildings.
        Here we are using sets to store the important buildings and creating those sets by checking whether the distance between the apartments and the important buildings is less than a mile,
        and then we use the and operator in set notation to see buildings near the important buildings

        :return:
        """
        b1 = ImportantBuilding.objects.create(building_slug="test",
                                              building_name="The test",
                                              address=Address.objects.create(address1="773 S 3rd St", zip_code="61020",
                                                                             city="Champaign", lat=Decimal(40.201),
                                                                             long=Decimal(-88.235970)))
        b2 = ImportantBuilding.objects.create(building_slug="test2",
                                              building_name="The test 2",
                                              address=Address.objects.create(address1="775 S 3rd St", zip_code="61020",
                                                                             city="Champaign", lat=Decimal(40.202),
                                                                             long=Decimal(-88.235970)))
        building_slugs = ['test','test2']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "the-suite")
        self.assertEqual(data[1]['apartment_slug'], "suite-life")
        self.assertEqual(len(data), 2)
        # Nearest apartment to both of these buildings is the-suite and suite-life at the moment

    def test_get_nearest_apartments_two(self):
        """
        Create two important buildings near some of the apartments and then tests the nearest apartments to the buildings.
        Here we are using sets to store the important buildings and creating those sets by checking whether the distance between the apartments and the important buildings is less than a mile,
        and then we use the and operator in set notation to see buildings near the important buildings

        In this case though, we are checking if some of the apartments near one important building is not near another important building and returns the number of important buildings near both

        :return:
        """
        b1 = ImportantBuilding.objects.create(building_slug="test",
                                              building_name="The test",
                                              address=Address.objects.create(address1="310 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.11),
                                                                long=Decimal(-88.247940)))
        b2 = ImportantBuilding.objects.create(building_slug="test2",
                                              building_name="The test 2",
                                              address=Address.objects.create(address1="341 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.13),
                                                                long=Decimal(-88.247940)))
        building_slugs = ['test','test2']
        starting_index = 0
        ending_index = 2
        print("Check nearest apartments 2")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data),0)
        # No nearest apartments within 1 mile of these two buildings as 308, although less than 1 mile via haversine, is more than 1 mile actual walking distance

    def test_get_nearest_apartments_three(self):
        """
        Create two important buildings near some of the apartments and then tests the nearest apartments to the buildings.
        Here we are using sets to store the important buildings and creating those sets by checking whether the distance between the apartments and the important buildings is less than a mile,
        and then we use the and operator in set notation to see buildings near the important buildings

        In this case though, we are checking if some of the apartments near one important building is not near another important building and returns the number of important buildings near both

        :return:
        """
        b1 = ImportantBuilding.objects.create(building_slug="test",
                                              building_name="The test",
                                              address=Address.objects.create(address1="310 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.11),
                                                                long=Decimal(-88.247940)))
        b2 = ImportantBuilding.objects.create(building_slug="test2",
                                              building_name="The test 2",
                                              address=Address.objects.create(address1="341 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.13),
                                                                long=Decimal(-88.247940)))
        building_slugs = ['test','test2']
        starting_index = 0
        ending_index = 2
        print("Check nearest apartments 2")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1.25"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "308")
        self.assertEqual(len(data),1)
        # Apartments within 1.25 miles of these two buildings is 308

    def test_get_nearest_apartments_biking(self):
        """

        :return:
        """
        b1 = ImportantBuilding.objects.create(building_slug="test",
                                              building_name="The test",
                                              address=Address.objects.create(address1="310 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.11),
                                                                long=Decimal(-88.247940)))
        b2 = ImportantBuilding.objects.create(building_slug="test2",
                                              building_name="The test 2",
                                              address=Address.objects.create(address1="341 Green St", zip_code="61020",
                                                                city="Champaign", lat=Decimal(40.13),
                                                                long=Decimal(-88.247940)))
        building_slugs = ['test','test2']
        starting_index = 0
        ending_index = 2
        print("Check nearest apartments 2")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=1.25"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data),0)
        # No apartments within 1.25 miles biking distance

    def test_get_nearest_apartments_biking_two(self):
        """
        Create two important buildings near some of the apartments and then tests the nearest apartments to the buildings.
        Here we are using sets to store the important buildings and creating those sets by checking whether the distance between the apartments and the important buildings is less than a mile,
        and then we use the and operator in set notation to see buildings near the important buildings

        :return:
        """
        b1 = ImportantBuilding.objects.create(building_slug="test",
                                              building_name="The test",
                                              address=Address.objects.create(address1="773 S 3rd St", zip_code="61020",
                                                                             city="Champaign", lat=Decimal(40.201),
                                                                             long=Decimal(-88.235970)))
        b2 = ImportantBuilding.objects.create(building_slug="test2",
                                              building_name="The test 2",
                                              address=Address.objects.create(address1="775 S 3rd St", zip_code="61020",
                                                                             city="Champaign", lat=Decimal(40.202),
                                                                             long=Decimal(-88.235970)))
        building_slugs = ['test','test2']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "the-suite")
        self.assertEqual(data[1]['apartment_slug'], "suite-life")
        self.assertEqual(len(data), 2)
        # Nearest apartment to both of these buildings is the-suite and suite-life at the moment

class NearestApartmentsTestTwo(APITestCase):
    def setUp(self):
        Apartment.objects.create(apartment_slug="207",
                                 apartment_name="207 S Fifth Street",
                                 address=Address.objects.create(address1="207 S Fifth St", zip_code="61820",
                                                                city="Champaign", lat=Decimal(40.114705328876),
                                                                long=Decimal(-88.23236328839553)),
                                 min_cost=600,
                                 max_cost=800,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/309-green"
                                 )

        Apartment.objects.create(apartment_slug="suites-at-third",
                                 apartment_name="Suites at Third",
                                 address=Address.objects.create(address1="707 S 3rd Street", zip_code="61820",
                                                                city="Champaign", lat=Decimal(40.1095247183999),
                                                                long=Decimal(-88.23583480189046)),
                                 min_cost=600,
                                 max_cost=800,
                                 website_url="https://www.americancampus.com/student-apartments/il/champaign/309-green"
                                 )

    def test_get_nearest_apartments_walk(self):
        """
        Walking distance of 1 mile from one important building

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments are 1 mile from Siebel
        
    def test_get_nearest_apartments_walk_two(self):
        """
        Walking distance of 0.5 miles from one important building

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=0.5"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(len(data), 1)
        # Only one apartment within 0.5 miles walking distance from Siebel

    def test_get_nearest_apartments_walk_three(self):
        """
        Walking distance of 0.45 miles from one important building

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=0.45"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(len(data), 1)
        # Only one apartment within 0.45 miles walking distance from Siebel

    def test_get_nearest_apartments_walk_four(self):
        """
        Walking distance of 0.25 miles from one important building

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=0.25"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)
        # No apartment within 0.25 walking distance from siebel

    def test_get_nearest_apartments_walk_five(self):
        """
        Walking distance of 2 miles from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=2"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments are within 2 miles from siebel and ARC

    def test_get_nearest_apartments_walk_six(self):
        """
        Walking distance of 1 mile from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 1)
        # Only suites-at-third within 1 mile walking dist from both Siebel and ARC

    def test_get_nearest_apartments_walk_seven(self):
        """
        Walking distance of 0.5 mile from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=0.5"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)
        # Only suites-at-third within 1 mile walking dist from both Siebel and ARC

    def test_get_nearest_apartments_bike_one(self):
        """
        

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments bike 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments within 1 mile biking distance from Siebel

    def test_get_nearest_apartments_bike_two(self):
        """
        

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments bike 2")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=0.5"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(len(data), 1)
        # One apartment within 0.5 mile biking distance from Siebel

    def test_get_nearest_apartments_bike_three(self):
        """
        

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments bike 3")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=0.4"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)
        # No apartments within 0.4 miles biking distance

    def test_get_nearest_apartments_bike_four(self):
        """
        Biking distance of 2 miles from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments bike 4")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=2"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments are within 2 miles from siebel and ARC

    def test_get_nearest_apartments_bike_five(self):
        """
        Biking distance of 1 mile from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments bike 5")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 1)
        # Only suites-at-third within 1 mile walking dist from both Siebel and ARC

    def test_get_nearest_apartments_bike_six(self):
        """
        Biking distance of 0.5 mile from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minBikingDist=0.5"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)
        # No apartment within 0.5 miles from both

    

    def test_get_nearest_apartments_drive_one(self):
        """
        Driving distance of 1 mile from one important building 

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minDrivingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments within 1 mile driving distance from Siebel

    def test_get_nearest_apartments_drive_two(self):
        """
        Driving distance of 0.5 miles from one important building

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minDrivingDist=0.5"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(len(data), 1)
        # Both apartments within 0.5 mile driving distance from Siebel

    def test_get_nearest_apartments_drive_three(self):
        """
        Driving distance of 0.4 from one important building

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        building_slugs = ['siebel']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minDrivingDist=0.4"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)
        # No apartment within 0.4 miles from siebel

    def test_get_nearest_apartments_drive_four(self):
        """
        Driving distance of 2 miles from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minDrivingDist=2"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments are within 2 miles from siebel and ARC

    def test_get_nearest_apartments_drive_five(self):
        """
        Driving distance of 1 mile from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minDrivingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 1)
        # Only suites-at-third within 1 mile walking dist from both Siebel and ARC

    def test_get_nearest_apartments_drive_six(self):
        """
        Driving distance of 0.5 mile from two important buildings

        :return:
        """
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minDrivingDist=0.5"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 0)
        # No apartment within 0.5 miles from both

    def test_get_nearest_apartments_walk_bike_one(self):
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1&minBikingDist=2"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments either within one mile walk or two mile bike from siebel or ARC

    def test_get_nearest_apartments_walk_bike_two(self):
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1&minBikingDist=1.5"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Both apartments either within one mile walk or 1.5 mile bike from siebel or ARC

    def test_get_nearest_apartments_walk_bike_three(self):
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1&minBikingDist=1"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 1)
        # Only Suites within one mile walk or 1 mile bike from siebel and ARC

    def test_get_nearest_apartments_walk_bike_drive_one(self):
        ImportantBuilding.objects.create(building_slug="siebel",
                                              building_name="Siebel Center for Computer Science",
                                              address=Address.objects.create(address1="201 N Goodwin Ave",
                                               zip_code="61801", 
                                               city="Urbana", 
                                               lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126')))

        ImportantBuilding.objects.create(building_slug="arc",
                                              building_name="ARC",
                                              address=Address.objects.create(address1="201 E Peabody Dr", 
                                              zip_code="61820",
                                               city="Champaign", 
                                               lat=Decimal('40.10201506403509'),
                                               long=Decimal('-88.2361043315809')))

        building_slugs = ['siebel', 'arc']
        starting_index = 0
        ending_index = 4
        print("Check nearest apartments 1")
        url = f"/api/get_nearest_apartments?buildingSlugs={json.dumps(building_slugs)}&starting_index={starting_index}&ending_index={ending_index}&universitySlug=UIUC&minWalkingDist=1&minBikingDist=1&minDrivingDist=2"
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        print("data: ", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]['apartment_slug'], "207")
        self.assertEqual(data[1]['apartment_slug'], "suites-at-third")
        self.assertEqual(len(data), 2)
        # Only Suites within one mile walk or 1 mile bike from siebel and ARC


class TestDistances(TestCase):
    def setUp(self) -> None:
        # ARC coords: (40.10201506403509, -88.2361043315809)
        Address.objects.create(address1="201 E Peabody Dr", zip_code="61820", city="Champaign", lat=Decimal('40.10201506403509'),
                               long=Decimal('-88.2361043315809'))
        # Thomas M Siebel Center for Computer Science coords: (40.11397506604104, -88.2249588393126)
        Address.objects.create(address1="201 N Goodwin Ave", zip_code="61801", city="Urbana", lat=Decimal('40.11397506604104'),
                               long=Decimal('-88.2249588393126'))

    # used Openrouteservice website and Google Maps to determine and confirm actual distances
    # testing with a margin of error of 0.05 mi (~80 meters) because it rounds distance to the nearest tenth
    def test_walking_dist(self):
        """
        Checks for distance between two addresses, and checks if the walking_dist function returns the proper walking distance
        :return:
        """
        arc = Address.objects.get(address1="201 E Peabody Dr", city="Champaign")
        siebel = Address.objects.get(address1="201 N Goodwin Ave", zip_code="61801")

        walking_dist = arc.get_walking_dist(siebel)

        self.assertTrue(math.isclose(walking_dist,1.4,abs_tol=0.05))
        # Used Openrouteservice website to determine actual walking distance 
    
    def test_biking_dist(self):
        """
        Checks for distance between two addresses, and checks if the walking_dist function returns the proper walking distance
        :return:
        """
        arc = Address.objects.get(address1="201 E Peabody Dr", city="Champaign")
        siebel = Address.objects.get(address1="201 N Goodwin Ave", zip_code="61801")

        biking_dist = arc.get_biking_dist(siebel)

        self.assertTrue(math.isclose(biking_dist,1.6,abs_tol=0.05))
        # Used Openrouteservice website to determine actual biking distance 

    def test_driving_dist(self):
        """
        Checks for distance between two addresses, and checks if the walking_dist function returns the proper walking distance
        :return:
        """
        arc = Address.objects.get(address1="201 E Peabody Dr", city="Champaign")
        siebel = Address.objects.get(address1="201 N Goodwin Ave", zip_code="61801")

        driving_dist = arc.get_driving_dist(siebel)

        self.assertTrue(math.isclose(driving_dist,1.6,abs_tol=0.05))
        # Used Openrouteservice website to determine actual driving distance 

    def test_transit_time(self):
        """
        Checks for distance between two addresses, and checks if the walking_dist function returns the proper walking distance
        :return:
        """
        arc = Address.objects.get(address1="201 E Peabody Dr", city="Champaign")
        siebel = Address.objects.get(address1="201 N Goodwin Ave", zip_code="61801")

        transit_time = arc.get_min_transit_time(siebel)

        print(transit_time)

        self.assertTrue((transit_time >= 13.433333333333334 and transit_time <= 20.96385542168675)) # approximately 16 minute travel time
