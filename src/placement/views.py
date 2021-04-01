from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from student.models import Student, Semester
from accounts.models import User
import json
from collections import OrderedDict
from django.core.mail import send_mail
import os

class InstituteAllView(generics.ListCreateAPIView):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer


class InstituteSingleView(APIView):

    def get(self, request, id):
        institute = Institute.objects.filter(id=id).first()
        if not institute:
            return HttpResponseNotFound()
        serializer = InstituteSerializer(institute)
        return Response(serializer.data)

#Security concern - Visible to any one
class JobApplicantsView (APIView):

    def get(self, request, id):
        try:
            jobProfile = JobProfile.objects.get(id=id)
        except JobProfile.DoesNotExist:
            return Response("Job profile with given id does not exist")
        jobApplicants = JobApplicant.objects.filter(job_profile=jobProfile)
        serializer = JobApplicantSerializer(jobApplicants, many=True)
        return Response(serializer.data)

class CancelJobsApplication (APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to cancel your application")
        for jobProfileJson in request.data:
            try:
                jobProfile = JobProfile.objects.get(id=jobProfileJson['id'])
            except JobProfile.DoesNotExist:
                jobProfile = None
            if (jobProfile == None):
                return Response("Invalid job profile")
            JobApplicant.objects.filter(student=student, job_profile=jobProfile).delete()
        return Response("Done")

class JobsApply (APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to apply")
        for jobProfileJson in request.data:
            try:
                jobProfile = JobProfile.objects.get(id=jobProfileJson['id'])
            except JobProfile.DoesNotExist:
                jobProfile = None
            if (jobProfile == None):
                return Response("Invalid job profile")
            jobRounds = JobRound.objects.filter(job_profile=jobProfile)
            if (len(jobRounds) == 0):
                jobRound = JobRound(round_no=0, job_profile=jobProfile)
                jobRound.save()
            jobRounds = JobRound.objects.filter(job_profile=jobProfile)
            for jobRound in jobRounds:
                try:
                    jobApplicant = JobApplicant.objects.get(
                        student=student, job_profile=jobProfile, job_round=jobRound)
                except JobApplicant.DoesNotExist:
                    jobApplicant = None
                if (jobApplicant != None):
                    break
            if (jobApplicant == None):
                jobApplicant = JobApplicant(
                    student=student, job_profile=jobProfile, job_round=jobRound)
                jobApplicant.save()
        return Response("Done")

def GetNumberOfBacklogs(student):
    noOfBacklogs = 0
    semesters = Semester.objects.filter(student=student)
    for semester in semesters:
        noOfBacklogs += semester.number_of_backlogs
    return noOfBacklogs

def SendEmailToEligibleStudents(id):
    #Get job profile from job id
    try:
        jobProfile = JobProfile.objects.get(id=id)
    except JobProfile.DoesNotExist:
        return

    print(jobProfile.gender_allowed)
    #Get list of eligible students
    eligibleStudents = Student.objects.filter(cgpa__gte=jobProfile.min_cgpa, gender__in=jobProfile.gender_allowed)

    for student in eligibleStudents:
        print(student.id)

    return
    #filtering students based on their backlogs
    uneligibleIds = []
    for student in eligibleStudents:
        noOfBacklogs = GetNumberOfBacklogs(student)                 #Calculate backlogs
        if (noOfBacklogs > jobProfile.max_backlogs):
            uneligibleIds.append(student.id)
    eligibleStudents.filter(id__in=uneligibleIds).delete()

    print(uneligibleIds)

    recepients = []
    for student in eligibleStudents:
        recepients.append(student.user.email)

    print(recepients)

    subject = 'New Job opening'
    message = 'Hello\n\nYou are eligible for a new job. Please make sure to apply for the same before the deadline\n\nRegards\nPowerset team'
    send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)

class JobProfileView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to see the jobs")
        noOfBacklogs = GetNumberOfBacklogs(student)
        jobProfiles = JobProfile.objects.filter(
            min_cgpa__lte=student.cgpa, max_backlogs__gte=noOfBacklogs, gender_allowed__contains=student.gender)
        serializer = JobProfileReadSerializer(jobProfiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student, placement=Placement.objects.filter(
            name=request.data['placement']).first()).first()
        if not coordinator:
            return Response("Please log in as a coordinator to use this functionality")
        data = OrderedDict()
        data.update(request.data)
        company_id = Company.objects.filter(
            name=request.data['company']).first().id
        placement_id = Placement.objects.filter(
            name=request.data['placement']).first().id
        data.pop('company')
        data.pop('placement')
        data.pop('branches_eligible')
        data.pop('gender_allowed')
        data['company'] = company_id
        data['placement'] = placement_id
        data['branches_eligible'] = json.loads(
            request.data['branches_eligible'])
        data['gender_allowed'] = json.loads(request.data['gender_allowed'])
        serializer = JobProfileWriteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        jobProfile = serializer.save()
        SendEmailToEligibleStudents(jobProfile.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
