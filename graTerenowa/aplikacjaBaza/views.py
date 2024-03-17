from django.shortcuts import render
from .models import Users, Questions
from .serializer import UsersSerializer, QuestionsSerializer
from rest_framework import viewsets

# Create your views here.

class UsersViewSet(viewsets.ModelViewSet):
  queryset=Users.objects.all()
  serializer_class=UsersSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
  queryset=Questions.objects.all()
  serializer_class=QuestionsSerializer