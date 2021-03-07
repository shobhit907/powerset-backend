from django.urls import path
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('projects', views.ProjectsView, 'projects')
# urlpatterns = router.urls


urlpatterns = [
    path('institutes/', views.InstituteAllView.as_view()),
    path('institutes/<int:id>', views.InstituteSingleView.as_view()),
]
