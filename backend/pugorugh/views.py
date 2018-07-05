from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import Http404

from . import serializers
from .models import Dog, UserPref, UserDog


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class AllDogs(generics.ListAPIView):
    """
    GET all dogs for API testing purposes

    /api/dogs/

    """
    queryset = Dog.objects.all()
    serializer_class = serializers.DogSerializer


class SpecificDog(generics.RetrieveAPIView):
    """
    GET single dog for API testing purposes

    /api/dog/<pk>/

    """
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Dog.objects.filter(id=pk)


class GETNextDog(generics.RetrieveAPIView):
    """
    To get the next liked/disliked/undecided dog

    /api/dog/<pk>/liked/next/
    /api/dog/<pk>/disliked/next/
    /api/dog/<pk>/undecided/next/

    """
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user = self.request.user
        all_dogs = Dog.objects.all()
        # Return appropriate queryset based on URL parameter for preference
        decision = self.kwargs.get('decision')
        if decision == 'undecided':
            queryset = all_dogs.filter(
                userdog__status='u',
                userdog__user_id=user.id
            ).order_by('pk')
        elif decision == 'liked':
            queryset = all_dogs.filter(
                userdog__status='l',
                userdog__user_id=user.id
            ).order_by('pk')
        elif decision == 'disliked':
            queryset = all_dogs.filter(
                userdog__status='d',
                userdog__user_id=user.id
            ).order_by('pk')
        return queryset

    def get_object(self):
        """GET single Dog instance from above queryset
        and cycle through list one at a time"""
        pk = self.kwargs['pk']
        queryset = self.get_queryset()
        # GET first instance of Dog with a PK value > the URL
        next_dog = queryset.filter(id__gt=pk).first()
        # loop through list in UI
        if next_dog is None:
            # throw a 404 if no dogs fall into a particular userdog category
            if queryset.first() is None:
                raise Http404
            return queryset.first()
        return next_dog


class PUTUserDog(APIView):
    """
    To change the dog's status

    /api/dog/<pk>/liked/
    /api/dog/<pk>/disliked/
    /api/dog/<pk>/undecided/

    Documentation:
    http://www.django-rest-framework.org/tutorial/
    3-class-based-views/#using-generic-class-based-views

    """
    serializer_class = serializers.UserDogSerializer

    def get_object(self, request):
        pk = self.kwargs['pk']
        dog = Dog.objects.get(id=pk)
        decision = self.kwargs['decision']
        if decision == 'liked':
            decision = 'l'
        elif decision == 'disliked':
            decision = 'd'
        elif decision == "undecided":
            decision = "u"
        else:
            decision = "PROBLEM"
        obj, exists = UserDog.objects.update_or_create(
            user=self.request.user,
            dog=dog,
            defaults={
                'status': decision
            }
        )
        return obj

    def get(self, request, pk, *args, **kwargs):
        """GET current User's list of dogs by category"""
        snippet = self.get_object(self.request.user.id)
        serializer = serializers.UserDogSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """UPDATE current User's list of dogs by category"""
        snippet = self.get_object(self.request.user.id)
        serializer = serializers.UserDogSerializer(snippet, data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GETorPUTUserPref(APIView):
    """
    To change or set user preferences

    /api/user/preferences/

    Documentation:
    http://www.django-rest-framework.org/tutorial/
    3-class-based-views/#using-generic-class-based-views

    """
    # queryset = UserPref.objects.all()
    serializer_class = serializers.DogSerializer

    def get_object(self, request):
        """GET current user preferences for logged in user
        or create preferences for new user based on model default"""
        obj, exists = UserPref.objects.get_or_create(
            user=self.request.user,
            defaults={
                'user': self.request.user,
                # Obtains default values from UserPref model
                'age': UserPref._meta.get_field('age').get_default(),
                'gender': UserPref._meta.get_field('gender').get_default(),
                'size': UserPref._meta.get_field('size').get_default()
            }
        )
        if obj:
            obj.save()
        return obj

    def get(self, request):
        """GET current User Preferences"""
        snippet = self.get_object(self.request.user.id)
        serializer = serializers.UserPrefSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """UPDATE current User Preferences"""
        snippet = self.get_object(self.request.user.id)
        serializer = serializers.UserPrefSerializer(snippet, data=request.data)
        print(serializer)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
