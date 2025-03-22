from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
from django.template import loader
from monthlyexpenses.Custommessages import Custommessage
from monthlyexpenses.models import Source
from monthlyexpenses.serializers import SourceSerializer, UserRegistrationSerializer
from monthlyexpenses.utilities import *

# Create your views here.

class SourceAPIView(generics.CreateAPIView):
    serializer_class = SourceSerializer
    msg_obj = Custommessage()

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            source_obj = serializer.save()
            msg = self.msg_obj.created.format(obj="Source")
            return success(msg,{"id":source_obj.id})
        return serializer_error(serializer)
    
class ListSourceAPIView(generics.ListAPIView):
    serializer_class = SourceSerializer
    msg_obj = Custommessage()
    def get(self,request):
        sources = Source.objects.all().values()
        template = loader.get_template('source_list.html')
        context = {"sources":sources}
        return HttpResponse(template.render(context, request))
        # serializer = self.get_serializer(sources,many=True)
        # msg = self.msg_obj.listed.format(obj="Source")
        # return success(msg,serializer.data)
    

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
    


            
