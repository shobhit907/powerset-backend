from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework import status

from student.models import *
from student.serializers import *
from student.forms import *
import json
from collections import OrderedDict

class SocialProfilesView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        try:
            socialProfile = SocialProfile.objects.get(student=student)
        except SocialProfile.DoesNotExist:
            socialProfile = None
        if (socialProfile == None):
            return Response("No Social Profile found")
        serializer = SocialProfileSerializer(socialProfile)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        try:
            socialProfile = SocialProfile.objects.get(student=student)
        except SocialProfile.DoesNotExist:
            socialProfile = None
        if (socialProfile != None):
            socialProfile.delete()
        socialProfilesJson = request.data[0]
        socialProfilesJson['student'] = student
        socialProfiles = SocialProfile(**socialProfilesJson)
        socialProfiles.save()
        return Response('Done')

class SocialProfilesAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            socialProfiles = SocialProfile.objects.all()
            serializer = SocialProfileSerializer(socialProfiles, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class SocialProfilesVerify (APIView):
    def put(self, request, id):
        student = Student.objects.get(user=request.user)
        coordinator = Coordinator.objects.filter(student=student).first()
        if (not coordinator):
            return Response('You must be logged in as coordinator to verify a student\'s details', status=status.HTTP_401_UNAUTHORIZED)
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            student=None
            return Response("Student with given id does not exist", status=status.HTTP_400_BAD_REQUEST)
        try:
            socialProfile = SocialProfile.objects.get(student=student)
        except SocialProfile.DoesNotExist:
            socialProfile = None
            return Response("Social profile does not exist for this student so nothing to verify", status=status.HTTP_200_OK)
        socialProfile.is_verified = request.data['is_verified']
        socialProfile.verification_message = request.data['verification_message']
        socialProfile.save()
        return Response("Verified", status=status.HTTP_200_OK)