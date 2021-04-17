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
from student.utils import *

class ResumeView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        coordinator = Coordinator.objects.filter(student=student).first()
        if not coordinator and ((not student) or student.id != id):
            return Response('Unauthorized Access')
        student = Student.objects.filter(id=id).first()
        resumes = Resume.objects.filter(student=student)
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        resumeDict = OrderedDict()
        resumeDict.update(request.data)
        resumeDict['student']=student.id
        serialzer = ResumeSerializer(data=resumeDict)
        serialzer.is_valid(raise_exception=True)
        for resume in Resume.objects.filter(student=student):
            resume.is_latest = False
            resume.save()
        serialzer.save()
        return Response(serialzer.data,status.HTTP_201_CREATED)

class ResumesAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            resumes = Resume.objects.all()
            serializer = ResumeSerializer(resumes, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class ResumesVerify (APIView):
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
        resumes = Resume.objects.filter(student=student)
        for resume in resumes:
            resume.is_verified = request.data['is_verified']
            resume.verification_message = request.data['verification_message']
            resume.save()
        verified = 'verified' if request.data['is_verified'] == "V" else 'rejected'
        SendVerificationMail('Resumes details', student.user.email, verified, str(coordinator.student.user.name), request.data['verification_message'])
        return Response("Verified", status=status.HTTP_200_OK)