from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework import status

from .models import *
from placement.models import Coordinator, Placement
from .serializers import *
from serializers_common import StudentReadSerializer
from .forms import *
import json
from collections import OrderedDict
from django.shortcuts import get_object_or_404

# Create your views here.

class ApiTestView (APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentReadSerializer(student, many=True)
        return Response(serializer.data)

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
        student = get_object_or_404(Student, user=request.user)
        coordinators = Coordinator.objects.filter(student=student)
        if not coordinators:
            return Response("Unauthorized access", status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.action = 'create'
        data = OrderedDict()
        data.update(request.data)
        data['user'] = request.user.id
        if 'institute' in data:
            del data['institute']
            data['institute'] = Institute.objects.filter(
                name=request.data['institute']).first().id
        if 'placement' in data:
            del data['placement']
            data['placement'] = Placement.objects.filter(
                name=request.data['placement']).first().id
        try:
            student = Student.objects.get(entry_number=data['entry_number'])
            if (request.user.id != student.id):
                return Response("Unauthorized access", status=stauts.HTTP_401_UNAUTHORIZED)
            serializer = StudentWriteSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response("Done", status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(StudentReadSerializer(Student.objects.filter(user=request.user).first()).data, status=status.HTTP_201_CREATED, headers=headers)

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
