from rest_framework import routers
from .views import *
from django.urls import path, include

router= routers.DefaultRouter()

router.register(r'users', UsersViewSet)
router.register(r'groups', GroupsViewSet)
router.register(r'group-members', GroupMembersViewSet)
router.register(r'locations', LocationsViewSet)

router.register(r'questions', QuestionsViewSet)
router.register(r'answers', AnswersViewSet)
router.register(r'user-answers', UserAnswersViewSet)



urlpatterns = [
  path('api/', include(router.urls)),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  path('login/', LoginView.as_view(), name='login'),
]