from django.urls import path
from . import views
from .other_views import project_views, patent_views, social_profiles_views, document_views, resume_views, awards_and_recognitions_views, work_experience_views, course_views
from .other_views import competition_views, certification_views, positions_of_responsibility_views, semester_views, class_views, conference_and_workshop_views
from .other_views import communication_language_views, exam_views
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
    path('<int:id>/work-experiences/', work_experience_views.WorkExperienceView.as_view()),
    path('<int:id>/work-experiences/verify/', work_experience_views.WorkExperienceVerify.as_view()),
    path('work-experiences/', work_experience_views.WorkExperiencesAllView.as_view()),
    path('', views.StudentAllView.as_view()),
    path('me/', views.StudentMeView.as_view()),
    path('<int:id>/', views.StudentSingleView.as_view()),
    path('<int:id>/awards-and-recognitions/', awards_and_recognitions_views.AwardAndRecognitionView.as_view()),
    path('<int:id>/awards-and-recognitions/verify/', awards_and_recognitions_views.AwardAndRecognitionsVerify.as_view()),
    path('awards-and-recognitions/', awards_and_recognitions_views.AwardAndRecognitionsAllView.as_view()),
    path('<int:id>/courses/', course_views.CourseView.as_view()),
    path('<int:id>/courses/verify/', course_views.CoursesVerify.as_view()),
    path('courses/', course_views.CoursesAllView.as_view()),
    path('<int:id>/competitions/', competition_views.CompetitionView.as_view()),
    path('<int:id>/competitions/verify/', competition_views.CompetitionsVerify.as_view()),
    path('competitions/', competition_views.CompetitionsAllView.as_view()),
    path('<int:id>/certifications/', certification_views.CertificationView.as_view()),
    path('<int:id>/certifications/verify/', certification_views.CertificationsVerify.as_view()),
    path('certifications/', certification_views.CertificationsAllView.as_view()),
    path('<int:id>/documents/', document_views.DocumentView.as_view()),
    path('<int:id>/documents/verify/', document_views.DocumentsVerify.as_view()),
    path('documents/', document_views.DocumentsAllView.as_view()),
    path('<int:id>/resumes/', resume_views.ResumeView.as_view()),
    path('<int:id>/resumes/verify/', resume_views.ResumesVerify.as_view()),
    path('resumes/', resume_views.ResumesAllView.as_view()),
    path('<int:id>/social-profiles/', social_profiles_views.SocialProfilesView.as_view()),
    path('<int:id>/social-profiles/verify/', social_profiles_views.SocialProfilesVerify.as_view()),
    path('social-profiles/', social_profiles_views.SocialProfilesAllView.as_view()),
    path('<int:id>/positions-of-responsibilities/', positions_of_responsibility_views.PositionOfResponsibiltyView.as_view()),
    path('<int:id>/positions-of-responsibilities/verify/', positions_of_responsibility_views.positionsOfResponsibilitiesVerify.as_view()),
    path('positions-of-responsibilities/', positions_of_responsibility_views.PositionOfResponsibiltiesAllView.as_view()),
    path('<int:id>/semesters/', semester_views.SemesterView.as_view()),
    path('<int:id>/semesters/verify/', semester_views.SemestersVerify.as_view()),
    path('semesters/', semester_views.SemestersAllView.as_view()),
    path('<int:id>/classes/', class_views.ClassView.as_view()),
    path('<int:id>/classes/verify/', class_views.ClassesVerify.as_view()),
    path('classes/', class_views.ClassesAllView.as_view()),
    path('<int:id>/conferences-and-workshops/', conference_and_workshop_views.ConferencesAndWorkshopView.as_view()),
    path('<int:id>/conferences-and-workshops/verify/', conference_and_workshop_views.ConferencesAndWorkshopsVerify.as_view()),
    path('conferences-and-workshops/', conference_and_workshop_views.ConferencesAndWorkshopsAllView.as_view()),
    path('<int:id>/communication-languages/', communication_language_views.CommunicationLanguageView.as_view()),
    path('communication-languages/', communication_language_views.CommunicationLanguagesAllView.as_view()),
    path('<int:id>/exams/', exam_views.ExamView.as_view()),
    path('<int:id>/exams/verify', exam_views.ExamsVerify.as_view()),
    path('exams/', exam_views.ExamsAllView.as_view()),
]
