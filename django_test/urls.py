from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django_test import views

urlpatterns = [
    path('molong/', views.MolongList.as_view()),
    path('molong/<int:pk>/', views.MolongDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)