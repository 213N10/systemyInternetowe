from django.shortcuts import render
from .models import Questions
from django.contrib.auth.models import User
from .serializer import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.

class UsersViewSet(viewsets.ModelViewSet):
  #queryset=User.objects.all()
  serializer_class=UsersSerializer
  queryset = User.objects.all()
  

class GroupsViewSet(viewsets.ModelViewSet):
  queryset=Groups.objects.all()
  serializer_class=GroupsSerializer


class GroupMembersViewSet(viewsets.ModelViewSet):
  queryset=GroupMembers.objects.all()
  serializer_class=GroupMembersSerializer

class LocationsViewSet(viewsets.ModelViewSet):
  queryset=Locations.objects.all()
  serializer_class=LocationsSerializer

class QuestionsViewSet(viewsets.ModelViewSet):
  queryset=Questions.objects.all()
  serializer_class=QuestionsSerializer

class AnswersViewSet(viewsets.ModelViewSet):
  queryset=Answers.objects.all()
  serializer_class=AnswersSerializer

class LoginView(APIView):

  permission_classes = []

  def post(self, request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
      token, _ = Token.objects.get_or_create(user=user)
      user_data = UsersSerializer(user).data
      return Response({"token": token.key, "user": user_data})
    else:
      return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)