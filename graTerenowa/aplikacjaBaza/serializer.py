from .models import Users, Groups, Questions, Locations
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Users
    fields = ['id','firstname', 'lastname']


class GroupsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Groups
    fields = ['id','name', 'points']


class QuestionsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Questions
    fields = ['id','location', 'pointsForQuestion', 'openQuestionMode','question']

class LocationsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Locations
    fields = ['id','name', 'description','latitude', 'longitude']