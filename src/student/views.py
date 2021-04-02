from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework import status

from .models import *
from .serializers import *
from .forms import *
import json
from collections import OrderedDict

# Create your views here.


class ApiTestView (APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentReadSerializer(student, many=True)
        return Response(serializer.data)


class ResumeView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
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

class DocumentView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        documents = Document.objects.filter(student=student)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        documentDict = OrderedDict()
        documentDict.update(request.data)
        documentDict['student']=student.id
        serialzer = DocumentSerializer(data=documentDict)
        serialzer.is_valid(raise_exception=True)
        serialzer.save()
        return Response(serialzer.data,status.HTTP_201_CREATED)

class DocumentsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            documents = Document.objects.all()
            serializer = DocumentSerializer(documents, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class StudentSingleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student).first()
        if not coordinator and (not student or student.id != id):
            return Response("Unauthorized access")
        student = Student.objects.filter(id=id).first()
        if not student:
            return HttpResponseNotFound(content='Not found')
        serializer = StudentReadSerializer(student)
        return Response(serializer.data)

    def put(self, request, id):
        student = Student.objects.filter(user=request.user).first()
        coordinator = Coordinator.objects.filter(student=student).first()
        if not coordinator and (not student or student.id != id):
            return Response("Unauthorized access")

        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            student = None
            return Response("Student with given id does not exist")

        serializer = StudentWriteSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Done", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = Student.objects.filter(user=request.user).first()
        if not student:
            return HttpResponseNotFound(content='Not found')
        serializer = StudentReadSerializer(student)
        return Response(serializer.data)

class StudentAllView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | IsAdminUser]
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentReadSerializer
        elif self.action == 'create':
            return StudentWriteSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        self.action = 'list'
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.action = 'create'
        data = OrderedDict()
        data.update(request.data)
        if 'institute' in data:
            del data['institute']
            data['institute'] = Institute.objects.filter(
                name=request.data['institute']).first().id
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(StudentReadSerializer(Student.objects.filter(user=request.user).first()).data, status=status.HTTP_201_CREATED, headers=headers)


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

class ProjectView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        projects = Project.objects.filter(student=student)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        Project.objects.filter(student=student).delete()
        for projectJson in request.data:
            projectJson['student'] = student
            project = Project(**projectJson)
            project.save()
        return Response('Done')

class ProjectsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class PatentView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        patents = Patent.objects.filter(student=student)
        serializer = PatentSerializer(patents, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        Patent.objects.filter(student=student).delete()
        for patentJson in request.data:
            patentJson['student'] = student
            patent = Patent(**patentJson)
            patent.save()
        return Response('Done')

class PatentsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            patents = Patent.objects.all()
            serializer = PatentSerializer(patents, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class AwardAndRecognitionView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
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
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        AwardAndRecognition.objects.filter(student=student).delete()
        for awardAndRecognitionJson in request.data:
            awardAndRecognitionJson['student'] = student
            awardAndRecognition = AwardAndRecognition(
                **awardAndRecognitionJson)
            awardAndRecognition.save()
        return Response('Done')

class AwardAndRecognitionsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            awardAndRecognitions = AwardAndRecognition.objects.all()
            serializer = AwardAndRecognitionSerializer(awardAndRecognitions, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class WorkExperienceView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        workExperiences = WorkExperience.objects.filter(student=student)
        serializer = WorkExperienceSerializer(workExperiences, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        WorkExperience.objects.filter(student=student).delete()
        for workExperienceJson in request.data:
            workExperienceJson['student'] = student
            workExperience = WorkExperience(**workExperienceJson)
            workExperience.save()
        return Response('Done')

class WorkExperiencesAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            workExperiences = WorkExperience.objects.all()
            serializer = WorkExperienceSerializer(workExperiences, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class CourseView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        courses = Course.objects.filter(student=student)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        Course.objects.filter(student=student).delete()
        for courseJson in request.data:
            courseJson['student'] = student
            courseJson = Course(**courseJson)
            courseJson.save()
        return Response('Done')

class CoursesAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class CompetitionView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        competitions = Competition.objects.filter(student=student)
        serializer = CompetitionSerializer(competitions, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        Competition.objects.filter(student=student).delete()
        for competitionJson in request.data:
            competitionJson['student'] = student
            competitionJson = Competition(**competitionJson)
            competitionJson.save()
        return Response('Done')

class CompetitionsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            competitions = Competition.objects.all()
            serializer = CompetitionSerializer(competitions, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class CertificationView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        certifications = Certification.objects.filter(student=student)
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        Certification.objects.filter(student=student).delete()
        for certificationJson in request.data:
            certificationJson['student'] = student
            certificationJson = Certification(**certificationJson)
            certificationJson.save()
        return Response('Done')

class CertificationsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            certifications = Certification.objects.all()
            serializer = CertificationSerializer(certifications, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class PositionOfResponsibiltyView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        positionOfResponsibility = PositionsOfResponsibility.objects.filter(
            student=student)
        serializer = PositionsOfResponsibilitySerializer(
            positionOfResponsibility, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        PositionsOfResponsibility.objects.filter(student=student).delete()
        for positionOfResponsibilityJson in request.data:
            positionOfResponsibilityJson['student'] = student
            positionOfResponsibility = PositionsOfResponsibility(
                **positionOfResponsibilityJson)
            positionOfResponsibility.save()
        return Response('Done')

class PositionOfResponsibiltiesAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            positionOfResponsibility = PositionsOfResponsibility.objects.all()
            serializer = PositionsOfResponsibilitySerializer(
                positionOfResponsibility, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

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

class ClassView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        classObject = Class.objects.filter(student=student)
        serializer = ClassSerializer(classObject, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        Class.objects.filter(student=student).delete()
        for classObjectJson in request.data:
            classObjectJson['student'] = student
            classObject = Class(**classObjectJson)
            classObject.save()
        return Response('Done')

class ClassesAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            classObject = Class.objects.all()
            serializer = ClassSerializer(classObject, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

class ConferencesAndWorkshopView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        conferencesAndWorkshops = ConferencesAndWorkshop.objects.filter(
            student=student)
        serializer = ConferencesAndWorkshopSerializer(
            conferencesAndWorkshops, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        ConferencesAndWorkshop.objects.filter(student=student).delete()
        for conferencesAndWorkshopsJson in request.data:
            conferencesAndWorkshopsJson['student'] = student
            conferencesAndWorkshops = ConferencesAndWorkshop(
                **conferencesAndWorkshopsJson)
            conferencesAndWorkshops.save()
        return Response('Done')

class ConferencesAndWorkshopsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            conferencesAndWorkshops = ConferencesAndWorkshop.objects.all()
            serializer = ConferencesAndWorkshopSerializer(
                conferencesAndWorkshops, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

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

class ExamView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        student = Student.objects.get(user=request.user)
        if ((not student) or student.id != id):
            return Response('Unauthorized Access')
        exams = Exam.objects.filter(student=student)
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id and request.user.get_username() != 'admin@gmail.com'):
            return Response('Unauthorized Access')
        Exam.objects.filter(student=student).delete()
        for examsJson in request.data:
            examsJson['student'] = student
            exams = Exam(**examsJson)
            exams.save()
        return Response('Done')

class ExamsAllView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.get_username() == 'admin@gmail.com':
            exams = Exam.objects.all()
            serializer = ExamSerializer(exams, many=True)
            return Response(serializer.data)
        else:
            return Response('You must be logged in as admin to perform this action')

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
