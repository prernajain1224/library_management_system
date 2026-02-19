from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role")

    class Meta:
        model = User
        fields = ['id','username','role']


class CreateUserSerializer(serializers.ModelSerializer):
    # role = serializers.CharField(write_only=True)

    # class Meta:
    #     model = User
    #     fields = ['username','role','password']


    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['LIBRARIAN','STUDENT'])

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id','name','author','is_available']
