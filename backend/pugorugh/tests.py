from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from .models import User, Dog, UserDog, UserPref
from .views import AllDogs, SpecificDog, GETNextDog

# Create your tests here.


class DogTestCase(TestCase):
    """Test the creation of a Dog object"""
    def setUp(self):
        Dog.objects.create(
            name="Sammy",
            image_filename="sammy.jpg",
            breed="Bernese Mountain Dog",
            age=12,
            user_pref_age="b",
            gender="m",
            size="xl",
        )

    def test_dog_creation(self):
        dog = Dog.objects.get(name="Sammy")
        self.assertEqual(dog.size, "xl")


class UserDogTestCase(TestCase):
    """Test the creation of a user's opinion of a particular dog"""
    def setUp(self):
        User.objects.create(
            username="unittest"
        )
        user = User.objects.get(id=1)

        Dog.objects.create(
            name="Sammy",
            image_filename="sammy.jpg",
            breed="Bernese Mountain Dog",
            age=12,
            user_pref_age="b",
            gender="m",
            size="xl",
        )

        dog = Dog.objects.get(id=1)

        UserDog.objects.create(
            user=user,
            dog=dog,
            status="l"
        )

    def test_user_dog_creation(self):
        userdog = UserDog.objects.get(dog=1)
        self.assertEqual(userdog.status, "l")


class UserPrefTestCase(TestCase):
    """Test the creation of a user's preference for dogs"""
    def setUp(self):
        User.objects.create(
            username="unittest"
        )
        user = User.objects.get(id=1)

        UserPref.objects.create(
            user=user,
            age=60,
            gender="f",
            size="s"
        )

    def test_user_preference_creation(self):
        userpref = UserPref.objects.get(user=1)
        self.assertNotEqual(userpref.size, "not a valid value")


class ViewsTestCase(APITestCase):
    """Test the three main views for cycling through dogs,
    choosing a status, and setting preferences"""
    def setUp(self):
        Dog.objects.create(
            name="Sammy",
            image_filename="sammy.jpg",
            breed="Bernese Mountain Dog",
            age=12,
            user_pref_age="b",
            gender="m",
            size="xl",
        )
        dog = Dog.objects.get(id=1)

        User.objects.create(
            username="unittest"
        )
        user = User.objects.get(id=1)

        UserPref.objects.create(
            user=user,
            age=60,
            gender="f",
            size="s"
        )

        UserDog.objects.create(
            user=user,
            dog=dog,
            status="l"
        )

    def test_AllDogs_view(self):
        factory = APIRequestFactory()
        user = User.objects.get(username="unittest")
        view = AllDogs.as_view()
        request = factory.get('all-dogs')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_SpecificDog_view(self):
        factory = APIRequestFactory()
        user = User.objects.get(username="unittest")
        view = SpecificDog.as_view()
        request = factory.get('specific-dog')
        force_authenticate(request, user=user)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GETorPUTUserPref_view(self):
        factory = APIRequestFactory()
        user = User.objects.get(username="unittest")
        view = AllDogs.as_view()
        request = factory.get('userpref')
        force_authenticate(request, user=user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GETNextDog_view(self):
        factory = APIRequestFactory()
        user = User.objects.get(username="unittest")
        view = GETNextDog.as_view()
        request = factory.get('next')
        force_authenticate(request, user=user)
        response = view(request, pk=1, decision='undecided')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_PUTUserDog_view(self):
        factory = APIRequestFactory()
        user = User.objects.put(username="unittest")
        view = AllDogs.as_view()
        request = factory.get('decide')
        force_authenticate(request, user=user, age=12, gender='m', size='l')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
