from django.contrib.auth.models import User
from rest_framework import serializers

from monthlyexpenses.models import Source


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"},write_only=True)

    def validate(self,validated_data):
        if validated_data.get("password2") != validated_data.get("password"):
            raise serializers.ValidationError({"password2":"Passwords didn't match."})
        return validated_data
    
    def create(self,validated_data):
        user = User.objects.create(username=validated_data.get("username"),
                            email=validated_data.get("email"),
                            password=validated_data.get("password"))
        
        return user

    class Meta:
        model = User
        fields = ['username','email','password','password2']




class SourceSerializer(serializers.ModelSerializer):
    label = serializers.CharField(max_length=30, required=True)

    def validate_label(self, label):
        if Source.objects.filter(label=label).exists():
            raise serializers.ValidationError("Source with this label already exist.")
        return label

    class Meta:
        model = Source
        fields = ("id","label",)
