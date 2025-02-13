from django.shortcuts import render
from rest_framework import generics

from monthlyexpenses.Custommessages import Custommessage
from monthlyexpenses.models import Source
from monthlyexpenses.serializers import SourceSerializer, UserRegistrationSerializer
from monthlyexpenses.utilities import *

# Create your views here.

class SourceAPIView(generics.ListCreateAPIView):
    serializer_class = SourceSerializer
    msg_obj = Custommessage()

    def post(self,request):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            source_obj = serializer.save()
            msg = self.msg_obj.created.format(obj="Source")
            return success(msg,{"id":source_obj.id})
        return serializer_error(serializer)
    
    def get(self,request):
        sources = Source.objects.all()
        serializer = self.get_serializer(sources,many=True)
        msg = self.msg_obj.listed.format(obj="Source")
        return success(msg,serializer.data)
    

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
            
