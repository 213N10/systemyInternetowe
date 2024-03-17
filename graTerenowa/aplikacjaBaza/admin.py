from django.contrib import admin
from django.http import request

from .models import Users, Groups, GroupMembers, Locations, Questions, Answers
from django.db.models.signals import pre_save
from django.contrib import messages
from django.dispatch import receiver

# Register your models here.
@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    search_fields = ['firstname', 'lastname']
    list_display = ['id', 'firstname', 'lastname']

@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'points']

@admin.register(GroupMembers)
class GroupMembersAdmin(admin.ModelAdmin):
    search_fields = ['group__name', 'user__firstname', 'user__lastname']
    list_display = ['group', 'user']

@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'latitude', 'longitude']

@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    search_fields = ['question']
    list_filter = ['openQuestionMode', 'pointsForQuestion', 'locations']
    list_display = ['id', 'question', 'locations', 'get_open_question_mode', 'pointsForQuestion']

    def get_open_question_mode(self, obj):
        return "Open Question" if obj.openQuestionMode else "Closed Question"

    get_open_question_mode.short_description = 'Question Mode'

@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_filter = ['status']
    search_fields = ['question__question', 'group__name']
    list_display = ['id', 'group', 'question', 'status', 'pointsForAnswer']

    def save_model(self, request, obj, form, change):
        # Sprawdzenie, czy pole odpowiedzi jest puste
        if obj.question.openQuestionMode:
            if not obj.openAnswer:
                self.message_user(request, "Open answer cannot be empty for this question!", level=messages.ERROR)
                return
            obj.closeAnswer = None
        else:
            if not obj.closeAnswer:
                self.message_user(request, "Close answer cannot be empty for this question!", level=messages.ERROR)
                return
            obj.openAnswer = None
        obj.save()

    def form_valid(self, form):
        if form.instance.question.openQuestionMode:
            if not form.cleaned_data['openAnswer']:
                self.message_user(request, "Open answer cannot be empty for this question!", level=messages.ERROR)
                return False
        else:
            if not form.cleaned_data['closeAnswer']:
                self.message_user(request, "Close answer cannot be empty for this question!", level=messages.ERROR)
                return False
        return super().form_valid(form)

@receiver(pre_save, sender=Answers)
def save_answer(sender, instance, **kwargs):
    # Sprawdzenie, czy pytanie jest otwarte czy zamknięte
    if instance.question.openQuestionMode:
        instance.openAnswer = instance.openAnswer  # Jeśli pytanie jest otwarte, ustaw odpowiedź
        instance.closeAnswer = None
    else:
        instance.closeAnswer = instance.closeAnswer  # Jeśli pytanie jest zamknięte, ustaw odpowiedź
        instance.openAnswer = None
