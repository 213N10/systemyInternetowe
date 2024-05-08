from .models import Groups, Questions, Locations, GroupMembers, Answers
from django.contrib.auth.models import User

from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = User
    fields = ['id','username', 'email', 'password', 'groups']

  def validate_email(self, mail):
    if User.objects.filter(email=mail).exists():
      raise serializers.ValidationError("Email already exists")
    return mail

  def create(self, validated_data):
    user = User(
      username=validated_data['username'],
      email=validated_data['email']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user


class GroupsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Groups
    fields = ['id','name', 'points']


class GroupMembersSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = GroupMembers
    fields = ['id','group', 'user']

class LocationsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Locations
    fields = ['id','name', 'description','latitude', 'longitude', 'QRcode']


class QuestionsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Questions
    fields = ['id','locations', 'question', 'openQuestionMode', 'pointsForQuestion', 'correctAnswer', 'correctAnswerInPosibleAnswers']


class AnswersSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Answers
    fields = ['group', 'question', 'openAnswer', 'closeAnswer', 'status', 'pointsForAnswer']

