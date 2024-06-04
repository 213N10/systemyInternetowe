from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

ANSWER_STATUS = (
    ('new', 'Waiting for check'),
    ('checked_positive', 'Answer correct'),
    ('checked_negative', 'Answer wrong')
)

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
    points_for_question = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    # Możliwe odpowiedzi
    option_1 = models.CharField(max_length=255, default='')
    option_2 = models.CharField(max_length=255, default='')
    option_3 = models.CharField(max_length=255, default='')
    option_4 = models.CharField(max_length=255, default='')
    # Poprawna odpowiedź
    correct_answer = models.CharField(max_length=1, choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')], default='1')

    def __str__(self):
        return self.question


    
# trzymane informacje o wszystkich odpowiedziach użytkowników
class UsersAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    question = models.CharField(max_length=255)
    result = models.BooleanField(default=False)
    points = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.user.username} - {self.question}"