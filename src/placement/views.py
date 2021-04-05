from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from serializers_common import JobApplicantSerializer
from rest_framework.permissions import IsAuthenticated
from student.models import Student, Semester
from accounts.models import User
import json
from collections import OrderedDict
from django.core.mail import send_mail
import os
from .utils import *

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

class JobApplicantsView (APIView):

    def get(self, request, id):
        try:
            jobProfile = JobProfile.objects.get(id=id)
        except JobProfile.DoesNotExist:
            return Response("Job profile with given id does not exist")
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student, placement=jobProfile.placement).first()
        if not coordinator:
            return Response("Please log in as a coordinator to use this functionality")
        jobApplicants = JobApplicant.objects.filter(job_profile=jobProfile)
        serializer = JobApplicantSerializer(jobApplicants, many=True)
        return Response(serializer.data)

class CancelJobsApplication (APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):
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

class JobProfileView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to see the jobs")
        coordinators = Coordinator.objects.filter(student=student)
        if not coordinators:
            noOfBacklogs = GetNumberOfBacklogs(student)
            jobProfiles = JobProfile.objects.filter(
                min_cgpa__lte=student.cgpa, max_backlogs__gte=noOfBacklogs, gender_allowed__contains=student.gender)
        else:
            jIds = []
            for coordinator in coordinators:
                jps = JobProfile.objects.filter(placement=coordinator.placement)
                for jp in jps:
                    jIds.append(jp.id)
            jobProfiles = JobProfile.objects.filter(id__in=jIds)
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
        SendEmailToEligibleStudents(jobProfile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AppliedJobsView (APIView):
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to see the jobs in which you have applied")
        jobApplications = JobApplicant.objects.filter(student=student)
        # jobIds = []
        # for j in jobApplications:
        #     jobIds.append(j.job_profile.id)
        # appliedJobs = JobProfile.objects.filter(id__in=jobIds)
        # serializer = JobProfileReadSerializer(appliedJobs, many=True)
        serializer = JobApplicantSerializer(jobApplications, many=True)
        return Response(serializer.data)

#Incomplete as of now
class UpdateApplicantRound (APIView):
    def put (self, request):
        try:
            jobProfile = JobProfile.objects.get(id=request.data['job_id'])
        except JobProfile.DoesNotExist:
            return Response("Job profile with given id does not exist")
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student, placement=jobProfile.placement).first()
        if not coordinator:
            return Response("Please log in as a coordinator to use this functionality")
        try:
            student = Student.objects.get(id=request.data['student_id'])
        except Student.DoesNotExist:
            student = None
            return Response("Invalid student id")
        try:
            jobApplicant = JobApplicant.objects.get(student=student, job_profile=jobProfile)
        except:
            jobApplicant = None
            return Response("Given student has not applied to the given job")
        currentRound = jobApplicant.job_round.round_no
        try:
            newRound = JobRound.objects.get(round_no=currentRound, job_profile=jobProfile)
        except JobRound.DoesNotExist:
            return Response("The candidate was already in the last round. So he is selected")