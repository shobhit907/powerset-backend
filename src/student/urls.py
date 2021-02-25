from django.urls import path
from . import views

urlpatterns = [
    path('', views.ApiTestView.as_view()),
    path('form_test/', views.FormTestView),
]