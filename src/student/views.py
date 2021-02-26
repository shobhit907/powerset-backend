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

class ProjectsView (APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if request.user.get_username() == 'admin@gmail.com':
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        else:
            student = Student.objects.get(user=request.user)
            if (student.id != id):
                return Response('Unauthorized Access')
            projects = Project.objects.filter(student=student)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)

    def post(self, request, id):
        student = Student.objects.get(user=request.user)
        if (student.id != id):
                return Response('Unauthorized Access')
        projects = Project.objects.filter(student=student).delete()
        for projectJson in request.data:
            projectJson['student'] = student
            project = Project(**projectJson)
            project.save()
        return Response('Done')

def FormTestView (request):

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = SocialProfileForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            # redirect to a new URL:
            return HttpResponseRedirect( )

    # If this is a GET (or any other method) create the default form.
    else:
        form = SocialProfileForm()

    context = {
        'form': form,
    }
    print(form)
    print(type(form))
    return render(request, 'formTest.html', context)