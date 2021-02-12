from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.

def getdata(request):
    data = {'name': 'powerset', 'coming_from': 'Django'}
    return JsonResponse(data=data)