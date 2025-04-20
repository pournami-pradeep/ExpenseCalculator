from django.contrib import admin
from django.urls import path
from monthlyexpenses import views

urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/', views.login_user, name='login'),
    path('source/',views.sources, name='source'),
    path('create-source/',views.create_source,name='create-source'),
    path('source-details/<int:source_id>/',views.source_detail,name='source-detail'),
    # path('delete-source/<int:source_id>/',views.delete_source,name='delete-source'),
    path('expense/<int:source_id>/',views.add_expense,name='expense'),
    path('',views.home, name="home"),
    # path('create-source/',views.CreateSource.as_view(),name='source-create'),
]