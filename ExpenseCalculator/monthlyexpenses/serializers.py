from django.contrib.auth.models import User
from rest_framework import serializers

from monthlyexpenses.models import Expenses, Source, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)

    def validate_email(self, email):
        if UserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exist.")
        return email

    def validate_name(self, val):
        if UserProfile.objects.filter(name=val).exists():
            raise serializers.ValidationError("Username already exist.")
        return val

    def create(self, validated_data):
        auth_user = User.objects.create(
            username=validated_data.get("name"), email=validated_data.get("email")
        )
        user = UserProfile.objects.create(
            name=validated_data.get("username"),
            email=validated_data.get("email"),
            profile_photo=validated_data.get("profile_photo"),
            user=auth_user,
        )

        return user

    class Meta:
        model = UserProfile
        fields = ["name", "email", "profile_photo"]


class SourceSerializer(serializers.ModelSerializer):
    label = serializers.CharField(max_length=30, required=True)

    def validate_label(self, label):
        if Source.objects.filter(label=label).exists():
            raise serializers.ValidationError("Source with this label already exist.")
        return label

    class Meta:
        model = Source
        fields = (
            "id",
            "label",
        )


class ExpenseSerializer(serializers.ModelSerializer):
    source = serializers.IntegerField(required=True)
    expense = serializers.IntegerField(required=True)

    def validate_source(self,value):
        try:
            source = Source.objects.get(id=value)
        except:
            raise serializers.ValidationError("Invalid Source")
        return source

    def validate_expense(self,value):
        if value < 0:
            raise serializers.ValidationError("Invalid")
        return value

    def create(self, validated_data):
        Expenses.objects.create(
            source=validated_data.get("source"), expense=validated_data.get("expense")
        )
        return True
    class Meta:
        model = Expenses
        fields = ("source", "expense")
