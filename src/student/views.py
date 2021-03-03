from django.shortcuts import render
#from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import APIView
from .models import *
from .serializers import *
from .forms import *
from rest_framework.permissions import IsAuthenticated
import json

# Create your views here.


class ApiTestView (APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)


class SocialProfilesView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            socialProfiles = SocialProfile.objects.all()
            serializer = ProjectSerializer(socialProfiles, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            socialProfile = SocialProfile.objects.get(student=student)
            serializer = ProjectSerializer(socialProfile)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Project.objects.filter(student=student).delete()
        for projectJson in request.data:
            projectJson['student'] = student
            project = Project(**projectJson)
            project.save()
        return Response('Done')

class ProjectsView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            projects = Project.objects.filter(student=student)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Project.objects.filter(student=student).delete()
        for projectJson in request.data:
            projectJson['student'] = student
            project = Project(**projectJson)
            project.save()
        return Response('Done')


class PatentsView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            patents = Patent.objects.all()
            serializer = PatentSerializer(patents, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            patents = Patent.objects.filter(student=student)
            serializer = PatentSerializer(patents, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Patent.objects.filter(student=student).delete()
        for patentJson in request.data:
            patentJson['student'] = student
            patent = Patent(**patentJson)
            patent.save()
        return Response('Done')


class AwardAndRecognitionsView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            awardAndRecognitions = AwardAndRecognition.objects.all()
            serializer = AwardAndRecognitionSerializer(
                awardAndRecognitions, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            awardAndRecognitions = AwardAndRecognition.objects.filter(
                student=student)
            serializer = AwardAndRecognitionSerializer(
                awardAndRecognitions, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        AwardAndRecognition.objects.filter(student=student).delete()
        for awardAndRecognitionJson in request.data:
            awardAndRecognitionJson['student'] = student
            awardAndRecognition = AwardAndRecognition(
                **awardAndRecognitionJson)
            awardAndRecognition.save()
        return Response('Done')


class WorkExperienceView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            workExperiences = WorkExperience.objects.all()
            serializer = WorkExperienceSerializer(workExperiences, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            workExperiences = WorkExperience.objects.filter(student=student)
            serializer = WorkExperienceSerializer(workExperiences, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        WorkExperience.objects.filter(student=student).delete()
        for workExperienceJson in request.data:
            workExperienceJson['student'] = student
            workExperience = WorkExperience(**workExperienceJson)
            workExperience.save()
        return Response('Done')


class CourseView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            courses = Course.objects.filter(student=student)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Course.objects.filter(student=student).delete()
        for courseJson in request.data:
            courseJson['student'] = student
            courseJson = Course(**courseJson)
            courseJson.save()
        return Response('Done')


class CompetitionView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            competitions = Competition.objects.all()
            serializer = CompetitionSerializer(competitions, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            competitions = Competition.objects.filter(student=student)
            serializer = CompetitionSerializer(competitions, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Competition.objects.filter(student=student).delete()
        for competitionJson in request.data:
            competitionJson['student'] = student
            competitionJson = Competition(**competitionJson)
            competitionJson.save()
        return Response('Done')


class CertificationView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            certifications = Certification.objects.all()
            serializer = CertificationSerializer(certifications, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            certifications = Certification.objects.filter(student=student)
            serializer = CertificationSerializer(certifications, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Certification.objects.filter(student=student).delete()
        for certificationJson in request.data:
            certificationJson['student'] = student
            certificationJson = Certification(**certificationJson)
            certificationJson.save()
        return Response('Done')

class PositionOfResponsibiltyView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            positionOfResponsibility = PositionsOfResponsibility.objects.all()
            serializer = PositionOfResponsibilitySerializer(positionOfResponsibility, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            positionOfResponsibility = positionOfResponsibility.objects.filter(student=student)
            serializer = PositionsOfResponsibilitySerializer(positionOfResponsibility, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        PositionsOfResponsibility.objects.filter(student=student).delete()
        for positionOfResponsibilityJson in request.data:
            positionOfResponsibilityJson['student'] = student
            positionOfResponsibility = PositionOfResponsibility(**positionOfResponsibilityJson)
            positionOfResponsibility.save()
        return Response('Done')

class SemesterView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            semester = Semester.objects.all()
            serializer = SemesterSerializer(semester, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            semester = Semester.objects.filter(student=student)
            serializer = SemesterSerializer(semester, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Semester.objects.filter(student=student).delete()
        for semesterJson in request.data:
            semesterJson['student'] = student
            semester = Semester(**semesterJson)
            semester.save()
        return Response('Done')

class ClassView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            classObject = Class.objects.all()
            serializer = ClassSerializer(classObject, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            classObject = Class.objects.filter(student=student)
            serializer = ClassrSerializer(classObject, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Class.objects.filter(student=student).delete()
        for classObjectJson in request.data:
            classObjectJson['student'] = student
            classObject = Class(**classObjectJson)
            classObject.save()
        return Response('Done')

class ConferencesAndWorkshopView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            conferencesAndWorkshops = ConferencesAndWorkshop.objects.all()
            serializer = ConferencesAndWorkshopSerializer(conferencesAndWorkshops, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            conferencesAndWorkshops = ConferencesAndWorkshop.objects.filter(student=student)
            serializer = ConferencesAndWorkshopSerializer(conferencesAndWorkshops, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        ConferencesAndWorkshop.objects.filter(student=student).delete()
        for conferencesAndWorkshopsJson in request.data:
            conferencesAndWorkshopsJson['student'] = student
            conferencesAndWorkshops = ConferencesAndWorkshop(**conferencesAndWorkshopsJson)
            conferencesAndWorkshops.save()
        return Response('Done')

class CommunicationLanguageView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            communicationLanguages = CommunicationLanguage.objects.all()
            serializer = CommunicationLanguageSerializer(communicationLanguages, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            communicationLanguages = CommunicationLanguage.objects.filter(student=student)
            serializer = CommunicationLanguageSerializer(communicationLanguages, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        CommunicationLanguage.objects.filter(student=student).delete()
        for communicationLanguagesJson in request.data:
            communicationLanguagesJson['student'] = student
            communicationLanguages = CommunicationLanguage(**communicationLanguagesJson)
            communicationLanguages.save()
        return Response('Done')

class ExamView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            exams = Exam.objects.all()
            serializer = ExamSerializer(exams, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if ((not student) or student.id != id):
                return Response('Unauthorized Access')
            exams = Exam.objects.filter(student=student)
            serializer = ExamSerializer(exams, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
            return Response('Unauthorized Access')
        Exam.objects.filter(student=student).delete()
        for examsJson in request.data:
            examsJson['student'] = student
            exams = Exam(**examsJson)
            exams.save()
        return Response('Done')

def FormTestView(request):

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SocialProfileForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            # redirect to a new URL:
            return HttpResponseRedirect()

    # If this is a GET (or any other method) create the default form.
    else:
        form = SocialProfileForm()

    context = {
        'form': form,
    }
    print(form)
    print(type(form))
    return render(request, 'formTest.html', context)
