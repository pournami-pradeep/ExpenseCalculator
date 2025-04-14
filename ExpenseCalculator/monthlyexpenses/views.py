from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from monthlyexpenses.Custommessages import Custommessage
from monthlyexpenses.models import Source
from rest_framework import generics

from .forms import SourceForm, UserRegistrationForm

# Create your views here.



def create_source(request):
    if not request.user.is_authenticated:
        return render(request,"page_not_found.html",{})
    if request.method == "POST":
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("source")
        error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
        return render(request,"source_create.html",{"form":form,"error":error_string})
    form = SourceForm()
    return render(request,"source_create.html",{"form":form})


def sources(request):
    if not request.user.is_authenticated:
        return render(request,"page_not_found.html",{})
    sources = Source.objects.all().values()
    context = {"sources":sources}
    return render(request,"source_list.html",context)


class ExpenseAPIView(generics.GenericAPIView):
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

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('source')  #should change this to source listing page
        return render(request,'login.html',{"error":"Error logging in."})
    return render(request,'login.html')
    


    


            
