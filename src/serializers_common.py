from rest_framework import serializers
from placement.serializers import InstituteSerializer, CoordinatorSerializer
from accounts.serializers import *
from student.models import Student, Resume
from placement.serializers import JobProfileReadSerializer, PlacementSerializer
from placement.models import JobApplicant, Coordinator
from student.serializers import ResumeSerializer
from django.shortcuts import get_object_or_404


class StudentReadSerializer (serializers.ModelSerializer):
    institute = InstituteSerializer()
    placement = PlacementSerializer()
    user = UserSerializer()
    coordinators = serializers.SerializerMethodField()
    primary_resume = serializers.SerializerMethodField()

    def get_coordinators(self, obj):
        coordinators_in = Coordinator.objects.filter(student=obj)
        serialized_data = CoordinatorSerializer(
            coordinators_in, many=True).data
        return serialized_data

    def get_primary_resume(self, obj):
        pr = Resume.objects.filter(student=obj, is_latest=True).first()
        return ResumeSerializer(pr).data

    class Meta:
        model = Student
        fields = ('id', 'entry_number', 'is_verified', 'branch', 'institute', 'user', 'degree', 'mother_name', 'placement', 'primary_resume',
                  'father_name', 'preferred_profile', 'category', 'technical_skills', 'introduction', 'career_plans', 'coordinators', 'batch', 'cgpa', 'verification_message')


class JobApplicantSerializer(serializers.ModelSerializer):

    student = StudentReadSerializer()
    job_profile = JobProfileReadSerializer()

    class Meta:
        model = JobApplicant
        fields = '__all__'
