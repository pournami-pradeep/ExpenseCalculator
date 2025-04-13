from django.contrib import admin
from django.urls import path
from monthlyexpenses import views

urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/', views.login_user, name='login'),
    path('source/',views.sources, name='source'),
    path('create-source/',views.create_source,name='create-source'),
    # path('expenses/<int:source_id>/',views.ExpenseAPIView.as_view(),name='expenses'),
    path('',views.HomePage.as_view(), name="home"),
    # path('create-source/',views.CreateSource.as_view(),name='source-create'),
]