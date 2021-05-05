from django.urls import path
from . import views
from rest_framework import routers

urlpatterns = [
    path('institutes/', views.InstituteAllView.as_view()),
    path('institutes/<int:id>/', views.InstituteSingleView.as_view()),
    path('job-profiles/<int:id>/applicants/', views.JobApplicantsView.as_view()),
    path('job-profiles/', views.JobProfileView.as_view()),
    path('job-profiles/<int:id>/', views.JobProfileSingleView.as_view()),
    path('job-profiles/all/', views.CoordinatorViewJobs.as_view()),
    path('apply/', views.JobsApply.as_view()),
    path('cancel/', views.CancelJobsApplication.as_view()),
    path('applied-jobs/', views.AppliedJobsView.as_view()),
    path('update-round/', views.UpdateApplicantRound.as_view()),
    path('reject/', views.RejectApplicantView.as_view()),
    path('companies/', views.CompanyAllView.as_view()),
]
