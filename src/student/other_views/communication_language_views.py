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

class CommunicationLanguageView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        communicationLanguages = CommunicationLanguage.objects.filter(
            student=student)
        serializer = CommunicationLanguageSerializer(
            communicationLanguages, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        CommunicationLanguage.objects.filter(student=student).delete()
        for communicationLanguagesJson in request.data:
            communicationLanguagesJson['student'] = student
            communicationLanguages = CommunicationLanguage(
                **communicationLanguagesJson)
            communicationLanguages.save()
        return Response('Done')

class CommunicationLanguagesAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            communicationLanguages = CommunicationLanguage.objects.all()
            serializer = CommunicationLanguageSerializer(
                communicationLanguages, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')