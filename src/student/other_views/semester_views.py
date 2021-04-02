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

class SemesterView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        semester = Semester.objects.filter(student=student)
        serializer = SemesterSerializer(semester, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        semesterDict = {}
        semesterDict['number'] = request.data['number']
        semesterDict['sgpa'] = request.data['sgpa']
        semesterDict['number_of_backlogs'] = request.data['number_of_backlogs']
        semesterDict['grade_sheet'] = request.data.get('file')
        semesterDict['student'] = student
        if (semesterDict.get('grade_sheet') == None):
            semester = Semester.objects.get(
                student=student, number=semesterDict['number'])
            semester.sgpa = semesterDict['sgpa']
            semester.number_of_backlogs = semesterDict['number_of_backlogs']
            semester.save()
        else:
            try:
                semester = Semester.objects.get(
                    student=student, number=semesterDict['number'])
            except Semester.DoesNotExist:
                semester = None
            if (semester != None):
                semester.delete()
            semester = Semester(**semesterDict)
            semester.save()
        return Response('Done')

class SemestersAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            semester = Semester.objects.all()
            serializer = SemesterSerializer(semester, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')
        
class SemestersVerify (APIView):
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
        semesters = Semester.objects.filter(student=student)
        for semester in semesters:
            semester.is_verified = request.data['is_verified']
            semester.save()
        return Response("Verified", status=status.HTTP_200_OK)