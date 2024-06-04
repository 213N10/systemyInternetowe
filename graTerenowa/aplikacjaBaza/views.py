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
import random
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class UsersViewSet(viewsets.ModelViewSet):
  #queryset=User.objects.all()
  serializer_class=UsersSerializer
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  queryset = User.objects.all()
  

class LocationsViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  queryset=Locations.objects.all()
  serializer_class=LocationsSerializer

class QuestionsViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  queryset=Questions.objects.all()
  serializer_class=QuestionsSerializer

  def get_queryset(self):
    queryset= super().get_queryset()
    locations = self.request.query_params.get('location',None)

    if locations is not None:
      queryset = queryset.filter(locations__name=locations)
    return queryset
  
  @action(detail=False, methods=['get'], url_path='random', url_name='random_question')
  def random_question(self, request):
    #location = request.query_params.get('location',None)
    queryset = self.get_queryset()

    if not queryset.exists():
      return Response({'error': 'No questions available'}, status=status.HTTP_404_NOT_FOUND)
    
    random_question = random.choice(queryset)
    serializer = QuestionsSerializer(random_question)
    return Response(serializer.data, status=status.HTTP_200_OK)


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
    

class UserAnswersViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]
  queryset=UsersAnswers.objects.all()
  serializer_class=UsersAnswersSerializer

  def get_queryset(self):
    queryset= super().get_queryset()
    user_id = self.request.query_params.get('user_id',None)

    if user_id is not None:
      queryset = queryset.filter(user__id=user_id)

    return queryset
  
  def create(self, request):
      serializer = UsersAnswersSerializer(data=request.data)
      if serializer.is_valid():
          try:
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          except Exception as e:
              return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
