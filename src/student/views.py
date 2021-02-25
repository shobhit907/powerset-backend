from django.shortcuts import render
#from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import APIView
from .models import Student
from .serializers import StudentSerializer
from .forms import *

# Create your views here.
class ApiTestView (APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

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

    return render(request, 'formTest.html', context)