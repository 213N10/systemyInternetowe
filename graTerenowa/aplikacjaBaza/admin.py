from django.contrib import admin
from django.http import request
from django.contrib.auth.models import User


from .models import Locations, Questions, UsersAnswers
from django.db.models.signals import pre_save
from django.contrib import messages
from django.dispatch import receiver

# Register your models here.



@admin.register(UsersAnswers)
class UsersAnswersAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'answer__question']
    list_display = ['id', 'user', 'question', 'points']


    def display_users(self,obj):
        return ", ".join([user.username for user in obj.users.all()])
    display_users.short_description = 'Users'

@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'latitude', 'longitude']


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('question', 'points_for_question')
    fieldsets = (
        (None, {
            'fields': ('locations', 'question', 'points_for_question')
        }),
        ('Odpowiedzi', {
            'fields': ('option_1', 'option_2', 'option_3', 'option_4', 'correct_answer'),
        }),
    )


