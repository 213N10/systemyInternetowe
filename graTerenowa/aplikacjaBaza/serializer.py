from .models import Questions, Locations, UsersAnswers
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = User
    fields = ['id','username', 'email', 'password']
    extra_kwargs = {
            'url': {'view_name': 'users-detail', 'lookup_field': 'id'}
        }

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
  def update(self, instance, validated_data):
    instance.username = validated_data.get('username', instance.username)
    instance.email = validated_data.get('email', instance.email)
    # Sprawdź, czy hasło zostało przesłane w danych uwierzytelnionych
    password = validated_data.get('password', None)
    if password is not None:
        instance.set_password(password)
    instance.save()
    return instance

    

class UsersAnswersSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UsersAnswers
        fields = ['id', 'user', 'question', 'points', 'result']

    def create(self, validated_data):
        user_instance = validated_data.pop('user')
        user_answer = UsersAnswers.objects.create(user=user_instance, **validated_data)
        return user_answer

class LocationsSerializer(serializers.HyperlinkedModelSerializer):
  class Meta():
    model = Locations
    fields = ['id','name', 'description','latitude', 'longitude', 'QRcode']


class QuestionsSerializer(serializers.HyperlinkedModelSerializer):
  locations = serializers.StringRelatedField()

  class Meta():
    model = Questions
    fields = ['id','locations', 'question', 'points_for_question', 'correct_answer', 'option_1', 'option_2', 'option_3', 'option_4']



