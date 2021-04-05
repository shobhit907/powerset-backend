from placement.serializers import InstituteSerializer, CoordinatorSerializer
from accounts.serializers import *
from student.models import Student
from placement.models import JobApplicant, Coordinator

class StudentReadSerializer (serializers.ModelSerializer):
    institute = InstituteSerializer()
    user = UserSerializer()
    coordinators = serializers.SerializerMethodField()

    def get_coordinators(self, obj):
        coordinators_in = Coordinator.objects.filter(student=obj)
        serialized_data = CoordinatorSerializer(
            coordinators_in, many=True).data
        return serialized_data

    class Meta:
        model = Student
        fields = ('id', 'entry_number', 'is_verified', 'branch', 'institute', 'user', 'degree', 'mother_name',
                  'father_name', 'preferred_profile', 'category', 'technical_skills', 'introduction', 'career_plans', 'coordinators')


class JobApplicantSerializer(serializers.ModelSerializer):

    student = StudentReadSerializer()

    class Meta:
        model = JobApplicant
        fields = '__all__'
