from django.contrib import admin
from django.urls import path

from monthlyexpenses import views

urlpatterns = [
    path('source/',views.SourceAPIView.as_view(),name='source'),
    path('register/',views.UserRegistrationAPIView.as_view(),name='source'),
]