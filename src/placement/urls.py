from django.urls import path
from . import views
from rest_framework import routers

urlpatterns = [
    path('institutes/', views.InstituteAllView.as_view()),
    path('institutes/<int:id>', views.InstituteSingleView.as_view()),
    path('job-profiles/<int:id>/applicants', views.JobApplicantsView.as_view()),
    path('job-profiles/', views.JobProfileView.as_view()),
    path('apply/', views.JobsApply.as_view()),
    path('cancel/', views.CancelJobsApplication.as_view()),
]
