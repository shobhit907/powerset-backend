from django.urls import path
from . import views
from .other_views import project_views, patent_views, social_profiles_views, document_views, resume_views, awards_and_recognitions_views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('projects', views.ProjectsView, 'projects')
# urlpatterns = router.urls


urlpatterns = [
    path('test_view/', views.ApiTestView.as_view()),
    path('form_test/', views.FormTestView),
    path('<int:id>/projects/', project_views.ProjectView.as_view()),
    path('<int:id>/projects/verify/', project_views.ProjectsVerify.as_view()),
    path('projects/', project_views.ProjectsAllView.as_view()),
    path('<int:id>/patents/', patent_views.PatentView.as_view()),
    path('<int:id>/patents/verify/', patent_views.PatentsVerify.as_view()),
    path('patents/', patent_views.PatentsAllView.as_view()),
    path('<int:id>/work-experiences/', views.WorkExperienceView.as_view()),
    path('work-experiences/', views.WorkExperiencesAllView.as_view()),
    path('', views.StudentAllView.as_view()),
    path('me/', views.StudentMeView.as_view()),
    path('<int:id>/', views.StudentSingleView.as_view()),

    path('<int:id>/awards-and-recognitions/', awards_and_recognitions_views.AwardAndRecognitionView.as_view()),
    path('<int:id>/awards-and-recognitions/verify/', awards_and_recognitions_views.AwardAndRecognitionsVerify.as_view()),
    path('awards-and-recognitions/', awards_and_recognitions_views.AwardAndRecognitionsAllView.as_view()),
    path('<int:id>/courses/', views.CourseView.as_view()),
    path('courses/', views.CoursesAllView.as_view()),
    path('<int:id>/competitions/', views.CompetitionView.as_view()),
    path('competitions/', views.CompetitionsAllView.as_view()),
    path('<int:id>/certifications/', views.CertificationView.as_view()),
    path('certifications/', views.CertificationsAllView.as_view()),
    path('<int:id>/documents/', document_views.DocumentView.as_view()),
    path('<int:id>/documents/verify/', document_views.DocumentsVerify.as_view()),
    path('documents/', document_views.DocumentsAllView.as_view()),
    path('<int:id>/resumes/', resume_views.ResumeView.as_view()),
    path('<int:id>/resumes/verify/', resume_views.ResumesVerify.as_view()),
    path('resumes/', resume_views.ResumesAllView.as_view()),
    path('<int:id>/social-profiles/', social_profiles_views.SocialProfilesView.as_view()),
    path('<int:id>/social-profiles/verify/', social_profiles_views.SocialProfilesVerify.as_view()),
    path('social-profiles/', social_profiles_views.SocialProfilesAllView.as_view()),
    path('<int:id>/positions-of-responsibilities/', views.PositionOfResponsibiltyView.as_view()),
    path('positions-of-responsibilities/', views.PositionOfResponsibiltiesAllView.as_view()),
    path('<int:id>/semesters/', views.SemesterView.as_view()),
    path('semesters/', views.SemestersAllView.as_view()),
    path('<int:id>/classes/', views.ClassView.as_view()),
    path('classes/', views.ClassesAllView.as_view()),
    path('<int:id>/conferences-and-workshops/', views.ConferencesAndWorkshopView.as_view()),
    path('conferences-and-workshops/', views.ConferencesAndWorkshopsAllView.as_view()),
    path('<int:id>/communication-languages/', views.CommunicationLanguageView.as_view()),
    path('communication-languages/', views.CommunicationLanguagesAllView.as_view()),
    path('<int:id>/exams/', views.ExamView.as_view()),
    path('exams/', views.ExamsAllView.as_view()),
]
