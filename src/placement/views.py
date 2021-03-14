from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from student.models import Student
import json
from collections import OrderedDict


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
        jobProfiles = JobProfile.objects.all()
        serializer = JobProfileReadSerializer(jobProfiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student, placement=Placement.objects.filter(
            name=request.data['placement']).first()).first()
        if not coordinator:
            return Response("Please log in as a coordinator to use this functionality")
        print(request.data['branches_eligible'])
        data = OrderedDict()
        data.update(request.data)
        company_id = Company.objects.filter(name=request.data['company']).first().id
        placement_id = Placement.objects.filter(name=request.data['placement']).first().id
        data.pop('company')
        data.pop('placement')
        data['company'] = company_id
        data['placement'] = placement_id
        serializer = JobProfileWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
