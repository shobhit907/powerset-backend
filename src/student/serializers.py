from django.db.models import fields
from rest_framework import serializers
from accounts.serializers import *
from placement.serializers import *
from .models import *

# Create your serializers here.
JSON_ALLOWED_OBJECTS = (dict, list, tuple, str, int, bool)


class StudentReadSerializer (serializers.ModelSerializer):
    institute = InstituteSerializer()
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ('id','entry_number', 'is_verified', 'branch', 'institute', 'user', 'degree', 'mother_name',
                  'father_name', 'preferred_profile', 'category', 'technical_skills', 'introduction', 'career_plans')


class StudentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CourseSerializer (serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AwardAndRecognitionSerializer (serializers.ModelSerializer):
    class Meta:
        model = AwardAndRecognition
        fields = '__all__'


class SocialProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model = SocialProfile
        fields = '__all__'


class ProjectSerializer (serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class PatentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Patent
        fields = '__all__'


class ResumeSerializer (serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class WorkExperienceSerializer (serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'


class CompetitionSerializer (serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = '__all__'


class PositionsOfResponsibilitySerializer (serializers.ModelSerializer):
    class Meta:
        model = PositionsOfResponsibility
        fields = '__all__'


class DocumentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class SemesterSerializer (serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class ClassSerializer (serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class CertificationSerializer (serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'


class ConferencesAndWorkshopSerializer (serializers.ModelSerializer):
    class Meta:
        model = ConferencesAndWorkshop
        fields = '__all__'


class CommunicationLanguageSerializer (serializers.ModelSerializer):
    class Meta:
        model = CommunicationLanguage
        fields = '__all__'


class ExamSerializer (serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class InstituteSerializer (serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'
