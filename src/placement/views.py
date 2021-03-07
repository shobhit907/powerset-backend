from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import APIView
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
import json

class InstituteAllView(generics.ListCreateAPIView):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer


class InstituteSingleView(APIView):
    
    def get(self, request, id):
        insitute = Institute.objects.filter(id=id).first()
        if not insitute:
            return HttpResponseNotFound()
        serializer = InstituteSerializer(insitute)
        return Response(serializer.data)

            