from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from rest_framework import generics

from monthlyexpenses.Custommessages import Custommessage
from monthlyexpenses.models import Source
from monthlyexpenses.serializers import (ExpenseSerializer, SourceSerializer,
                                         UserRegistrationSerializer)
from monthlyexpenses.utilities import *

from .forms import UserRegistrationForm

# Create your views here.

class CreateSource(generics.CreateAPIView):
    serializer_class = SourceSerializer

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()   
            return redirect('source')
        
        return render(request, "source_create.html", {
            "errors":"Source with this label already exist."
        })
        
    def get(self,request):
        return render(request, "source_create.html", {})

    

class SourceAPIView(generics.GenericAPIView):

    def get(self,request):
        sources = Source.objects.all().values()
        template = loader.get_template('source_list.html')
        context = {"sources":sources}
        return HttpResponse(template.render(context, request))
    

class ExpenseAPIView(generics.GenericAPIView):
    serializer_class = ExpenseSerializer
    msg_obj = Custommessage()

   
    def post(self,request,*args,**kwargs):
        source_id=self.kwargs.get("pk")
        source = get_object_or_404(Source, id=source_id)
        serializer = self.get_serializer(data=request.data,context={"source":source})
        if serializer.is_valid():
            msg = self.msg_obj.added
            return success(msg,{})
        return serializer_error(serializer)
    
    def get(self,request):
        source_id=self.kwargs.get("source_id")
        source = get_object_or_404(Source, id=source_id)
        return render(request, "expenses.html", {"source":source})
    

class HomePage(generics.GenericAPIView):
    def get(self,request):
        template = loader.get_template('home.html')
        return HttpResponse(template.render())


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                messages.success(request,"Logged in successfully.")
                return render(request, 'home.html',{})
        # messages.success(request,"Error logging in.")
        error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
        form = UserRegistrationForm(request.POST)
        return render(request, 'register.html',{"form":form,"error":error_string})
    form = UserRegistrationForm()
    return render(request, 'register.html',{"form":form})


class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    msg_obj = Custommessage()

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            msg = self.msg_obj.created.format(obj="User")
            return success(msg,{"id":user.id})
        return serializer_error(serializer)
    


            
