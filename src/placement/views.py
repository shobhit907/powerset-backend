from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import APIView
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from student.models import Student
import json

class InstituteAllView(generics.ListCreateAPIView):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer


class InstituteSingleView(APIView):
    
    def get(self, request, id):
        insitute = Institute.objects.filter(id=id).first()
        if not insitute:
            return HttpResponseNotFound()
        serializer = InstituteSerializer(insitute)
        return Response(serializer.data)

class JobProfileView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # student = Student.objects.filter(user=request.user).first()
        # try:
        #     coordinator = Coordinator.objects.get(student=student)
        # except Coordinator.DoesNotExist:
        #     coordinator = None
        # if (coordinator == None):
        #     return Response("Please log in as a coordinator to use this functionality")
        jobProfiles = JobProfile.objects.all()
        serializer = JobProfileSerializer(jobProfiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student,placement=request.data['placement']).first()
        if not coordinator:
            return Response("Please log in as a coordinator to use this functionality")
        # JobProfile.objects.all().delete()
        jobProfileJson=request.data
        jobProfileJson['company'] = Company.objects.filter(name=jobProfileJson['company']).first()
        jobProfileJson['placement'] = Placement.objects.filter(name=jobProfileJson['placement']).first()
        jobProfile = JobProfile(**jobProfileJson)
        jobProfile.save()
        return Response('Done')