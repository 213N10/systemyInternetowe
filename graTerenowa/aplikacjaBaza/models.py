from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

ANSWER_STATUS = (
    ('new', 'Waiting for check'),
    ('checked_positive', 'Answer correct'),
    ('checked_negative', 'Answer wrong')
)

"""class Users(models.Model):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)

    def __str__(self):
        return self.firstname + " " + self.lastname
"""
class Groups(models.Model):
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class GroupMembers(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Locations(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    QRcode = models.TextField()

    def __str__(self):
        return self.name

class Questions(models.Model):
    locations = models.ForeignKey(Locations, on_delete=models.CASCADE)
    question = models.TextField()
    openQuestionMode = models.BooleanField(default=True)
    correctAnswer = models.TextField(blank=True, null=True)
    correctAnswerInPosibleAnswers = models.CharField(max_length=1, blank=True, null=True)  # Może być puste
    pointsForQuestion = models.IntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return self.question

class Answers(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    openAnswer = models.TextField(blank=True, null=True)
    closeAnswer = models.CharField(max_length=1, blank=True, null=True)
    status = models.CharField(choices=ANSWER_STATUS, max_length=60 ,default='new')
    pointsForAnswer = models.IntegerField(validators=[MinValueValidator(0)],default=0)

    def __str__(self):
        return f"{self.group.name} - {self.question.question}"