from django.db.models import fields
from rest_framework import serializers
import rest_framework
from .models import *

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = '__all__'


class CoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinator
        fields = '__all__'


class JobProfileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfile
        fields = '__all__'
        depth = 1
        

class JobProfileWriteSerializer(serializers.ModelSerializer):

    branches_eligible = rest_framework.fields.MultipleChoiceField(choices=branch_choices)

    class Meta:
        model = JobProfile
        fields = '__all__'


class JobRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRound
        fields = '__all__'


class JobApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicant
        fields = '__all__'
