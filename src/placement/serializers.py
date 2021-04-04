from django.db.models import fields
from rest_framework import serializers, fields
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

    branches_eligible = fields.MultipleChoiceField(choices=branch_choices)
    gender_allowed = fields.MultipleChoiceField(choices=gender_choices)

    class Meta:
        model = JobProfile
        fields = '__all__'


class JobRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRound
        fields = '__all__'