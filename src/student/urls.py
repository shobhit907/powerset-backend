from django.urls import path
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('projects', views.ProjectsView, 'projects')
# urlpatterns = router.urls


urlpatterns = [
    path('', views.ApiTestView.as_view()),
    path('form_test/', views.FormTestView),
    path('<int:id>/projects/', views.ProjectsView.as_view()),
    path('<int:id>/patents/', views.PatentsView.as_view()),
    path('<int:id>/work-experiences/', views.WorkExperienceView.as_view()),
    path('<int:id>/awards-and-recognitions/', views.AwardAndRecognitionsView.as_view()),
    path('<int:id>/courses/', views.CourseView.as_view()),
    path('<int:id>/competitions/', views.CompetitionView.as_view()),
    path('<int:id>/certifications/', views.Certification.as_view()),
    
]