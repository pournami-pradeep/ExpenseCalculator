from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from rest_framework import generics

from monthlyexpenses.Custommessages import Custommessage

from monthlyexpenses.models import Source
from monthlyexpenses.serializers import (ExpenseSerializer, SourceSerializer,
                                         UserRegistrationSerializer)
from monthlyexpenses.utilities import *

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

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            msg = self.msg_obj.added
            return success(msg,{})
        return serializer_error(serializer)
    

class HomePage(generics.GenericAPIView):
    def get(self,request):
        template = loader.get_template('home.html')
        return HttpResponse(template.render())


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
    


            
