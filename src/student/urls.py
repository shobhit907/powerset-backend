from django.urls import path
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('projects', views.ProjectsView, 'projects')
# urlpatterns = router.urls


urlpatterns = [
    path('test_view/', views.ApiTestView.as_view()),
    path('form_test/', views.FormTestView),
    path('<int:id>/projects/', views.ProjectView.as_view()),
    path('<int:id>/patents/', views.PatentView.as_view()),
    path('<int:id>/work-experiences/', views.WorkExperienceView.as_view()),
    path('', views.StudentAllView.as_view()),
    path('<int:id>/', views.StudentSingleView.as_view()),

    path('<int:id>/awards-and-recognitions/',
         views.AwardAndRecognitionView.as_view()),
    path('<int:id>/courses/', views.CourseView.as_view()),
    path('<int:id>/competitions/', views.CompetitionView.as_view()),
    path('<int:id>/certifications/', views.CertificationView.as_view()),
    path('<int:id>/documents/', views.DocumentView.as_view()),
    path('<int:id>/resumes/', views.ResumeView.as_view()),
    path('<int:id>/social-profiles/', views.SocialProfilesView.as_view()),
    path('<int:id>/positions-of-responsibilities/',
         views.PositionOfResponsibiltyView.as_view()),
    path('<int:id>/semesters/', views.SemesterView.as_view()),
    path('<int:id>/classes/', views.ClassView.as_view()),
    path('<int:id>/conferences-and-workshops/',
         views.ConferencesAndWorkshopView.as_view()),
    path('<int:id>/communication-languages/',
         views.CommunicationLanguageView.as_view()),
    path('<int:id>/exams/', views.ExamView.as_view()),
]
