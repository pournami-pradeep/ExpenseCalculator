from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from monthlyexpenses.Custommessages import Custommessage
from monthlyexpenses.models import Expenses, Source
from rest_framework import generics

from .forms import ExpenseForm, SourceForm, UserRegistrationForm

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


def source_detail(request,source_id):
    try:
        source = Source.objects.get(id=source_id)
    except:
        return render(request,"page_not_found.html",{})
    
    expenses = Expenses.objects.filter(source=source)
    total_amount = sum(exp.expense for exp in expenses)
    print(total_amount,';;;;;;;;;;;;;;;;;;;;;;;;;;;;')
    context = {"source":source,"expense":expenses,"total_amount":total_amount}
    return render(request,"source_detail.html",context)

   
def add_expense(request,source_id):
    try:
        source = Source.objects.get(id=source_id)
    except:
        return render(request,"page_not_found.html",{})
    
    
    if request.method == "POST":
        form = ExpenseForm(request.POST,{"source":source})
        if form.is_valid():
            amount = form.cleaned_data["expense"]
            date = form.cleaned_data["date"]
            expense = Expenses(source=source,expense=amount,date=date) 
            expense.save()
            return redirect("source-detail",source_id)
            # return render(request,"source_detail.html",context)
        error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
        return render(request,"expense.html",{"form":form,"error":error_string})
    form = ExpenseForm()
    return render(request,"expense.html",{"form":form,"source":source})


def delete_expense(request,expense_id,source_id):
    try:
        expense = Expenses.objects.get(id=expense_id)
    except:
        return render(request,"page_not_found.html",{})
    expense.delete()
    return redirect("source-detail",source_id)


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


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        return redirect('source')
    return render(request,'home.html')


def delete_source(request,source_id):
    try:
        source = Source.objects.get(id=source_id)
    except:
        return render(request,"page_not_found.html",{})
    source.delete()
    return redirect('source')
    




    


    


            
