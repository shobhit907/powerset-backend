from functools import partial
from django.http.response import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
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
import datetime

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
            JobApplicant.objects.filter(student=student, job_profile=jobProfile, is_selected=False).delete()
            recepients = []
            recepients.append(jobApplicant.student.user.email)
            subject = 'Application cancelled for ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title)
            message = 'Dear Student,\n\nYour application for ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title) + ' was successfully cancelled. If this was not intended, please reapply immediately before the deadline - '+ str(jobProfile.end_date) + '.\n\nRegards\nPowerset team'
            send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)
        return Response("Done")

class JobsApply (APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to apply", status=status.HTTP_401_UNAUTHORIZED)

        #Some basics checks across all jobs so as to prevent any incomplete applications
        for jobProfileJson in request.data:
            try:
                jobProfile = JobProfile.objects.get(id=jobProfileJson['id'])
            except JobProfile.DoesNotExist:
                return Response("Invalid job profile", status=status.HTTP_400_BAD_REQUEST)

            if not IsStudentEligibleForJob(student, jobProfile):
                return Response ("You are forcefully trying to apply to jobs in which you are not eligible. This is not allowed.", status=status.HTTP_400_BAD_REQUEST)

        for jobProfileJson in request.data:
            jobProfile = JobProfile.objects.get(id=jobProfileJson['id'])

            #Checking if already applied in this job
            for jobRound in range(1, jobProfile.number_of_rounds+1):
                try:
                    jobApplicant = JobApplicant.objects.get(
                        student=student, job_profile=jobProfile, job_round=jobRound)
                except JobApplicant.DoesNotExist:
                    jobApplicant = None
                
                #If already applied then break
                if (jobApplicant != None):
                    break

            #If not applied then apply
            if (jobApplicant == None):
                jobApplicant = JobApplicant(
                    student=student, job_profile=jobProfile, job_round=1)
                jobApplicant.save()

                recepients = []
                recepients.append(jobApplicant.student.user.email)
                # recepients.append('rohittuli08@gmail.com')
                subject = 'Applied in ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title)
                message = 'Dear Student,\n\nThank you for applying in ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title) + '. The details and schedule of the shortlisting procedure are available for this job on the powerset portal.\n\nRegards\nPowerset team'
                send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)
        return Response("Done")

class CoordinatorViewJobs (APIView):

    def get (self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to see the jobs")
        coordinators = Coordinator.objects.filter(student=student)
        if not coordinators:
            return Response("Please log in as a coordinator to use this functionality")
        jIds = []
        for coordinator in coordinators:
            jps = JobProfile.objects.filter(placement=coordinator.placement)
            for jp in jps:
                jIds.append(jp.id)
        jobProfiles = JobProfile.objects.filter(id__in=jIds)
        serializer = JobProfileReadSerializer(jobProfiles, many=True)
        return Response(serializer.data)

class JobProfileSingleView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        try:
            jobProfile = JobProfile.objects.get(id=id)
        except JobProfile.DoesNotExist:
            return Response("Invalid job profile", status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student, placement=jobProfile.placement).first()
        if not coordinator and not IsStudentEligibleForJob(student, jobProfile):
            return Response("Unauthorized Access")

        jobProfileSerializer = JobProfileReadSerializer(jobProfile)
        return Response(jobProfileSerializer.data)

    def put(self, request, id):
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student, placement=Placement.objects.filter(
            name=request.data['placement']).first()).first()
        if not coordinator:
            return Response("Please log in as a coordinator to use this functionality")
        data = OrderedDict()
        data.update(request.data)
        try:
            company = Company.objects.get(name=request.data['company'])
        except Company.DoesNotExist:
            companyData = {}
            companyData['name'] = request.data['company']
            companySerializer = CompanySerializer(data=companyData)
            companySerializer.is_valid(raise_exception=True)
            company = companySerializer.save()
        company_id = company.id
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
        job= get_object_or_404(JobProfile, id=id)
        if not data.get('start_date'):
            data['start_date'] = job.start_date
        serializer = JobProfileWriteSerializer(job, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        jobProfile = serializer.save()
        SendEmailToEligibleStudents(jobProfile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobProfileView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        if (student == None):
            return Response("Please login as a valid student to see the jobs")
        if (student.is_selected):
            return Response("Student is already selected in a job so is now uneligible for appying in further jobs", status=status.HTTP_200_OK)
        if (student.is_verified != 'Verified'):
            return Response("Student is not verified and so uneligible for appying in jobs", status=status.HTTP_200_OK)
        noOfBacklogs = GetNumberOfBacklogs(student)
        jobProfiles = JobProfile.objects.filter(
            min_cgpa__lte=student.cgpa, max_backlogs__gte=noOfBacklogs, gender_allowed__contains=student.gender, branches_eligible__contains=student.branch, placement=student.placement, end_date__gte=datetime.date.today())
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
        try:
            company = Company.objects.get(name=request.data['company'])
        except Company.DoesNotExist:
            companyData = {}
            companyData['name'] = request.data['company']
            companySerializer = CompanySerializer(data=companyData)
            companySerializer.is_valid(raise_exception=True)
            company = companySerializer.save()
        company_id = company.id
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
        serializer = JobApplicantSerializer(jobApplications, many=True)
        return Response(serializer.data)

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

        if (jobApplicant.is_selected):
            return Response("Given student was already selected for this job")
            
        currentRound = jobApplicant.job_round
        newRound = currentRound + 1

        recepients = []
        recepients.append(jobApplicant.student.user.email)

        if (newRound > jobProfile.number_of_rounds):
            jobApplicant.is_selected = True
            jobApplicant.student.is_selected = True
            jobApplicant.save()
            jobApplicant.student.save()

            subject = 'Congratulations! Selected for ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title)
            message = 'Dear Student,\n\nCongratulations! We are glad to inform you that you have received an offer in ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title) + '.\n\nRegards\nPowerset team'
            send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)

            return Response("The candidate was already in the last round. So he is selected", status=status.HTTP_200_OK)

        subject = 'Shortlisted to the next round in ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title)
        message = 'Dear Student,\n\nWe are glad to inform you that you have been shortlisted for the next round in ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title) + '\n\nYour previous round: ' + str(currentRound) + '\nYour new round: ' + str(newRound) + '.\n\nRegards\nPowerset team'
        send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)

        jobApplicant.job_round = newRound
        jobApplicant.save()
        return Response("Done", status=status.HTTP_200_OK)

class RejectApplicantView (APIView):

    def delete (self, request):
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
        
        recepients = []
        recepients.append(student.user.email)

        JobApplicant.objects.filter(student=student, job_profile=jobProfile).delete()

        subject = 'Thank you for participating in ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title)
        message = 'Dear Student,\n\nWe regret to inform you that you are not shortlisted for next stage of ' + str(jobProfile.company) + '\'s Job Profile : ' + str(jobProfile.title) + '\n\nWe would like to wish you very best for future placements.\n\nRegards\nPowerset team'
        send_mail(subject, message, os.getenv('EMAIL_HOST_USER'), recepients, fail_silently = False)

        return Response("Done")

class CompanyData(object):
    def __init__(self, company, visit_date, leave_date, st):
        self.company = company
        self.visit_date = visit_date
        self.leave_date = leave_date
        self.company_status = st

class CompanyAllView (APIView):

    def get(self, request):
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student).first()
        if not coordinator:
            return Response("Please log in as a coordinator to use this functionality")
        companies = Company.objects.all()

        responseData = []

        for company in companies:
            jobProfiles=JobProfile.objects.filter(company=company)
            company_visit_date = min([job.start_date for job in jobProfiles])
            company_leave_date = max([job.end_date for job in jobProfiles])
            today = datetime.date.today()
            companyStatus=None
            if (company_visit_date <= today and company_leave_date >= today):
                companyStatus="present"
            elif (company_visit_date > today):
                companyStatus="future"
            else:
                companyStatus="past"
            companyData = CompanyData(company, company_visit_date, company_leave_date, companyStatus)
            responseData.append(companyData)

        return Response(CompanyDataSerializer(responseData, many=True).data, status=status.HTTP_200_OK)