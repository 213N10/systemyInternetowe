from rest_framework import routers
from .views import UsersViewSet, QuestionsViewSet
from django.urls import path, include

router= routers.DefaultRouter()

router.register(r'users', UsersViewSet)
router.register(r'questions', QuestionsViewSet)

urlpatterns = [
  path('api/', include(router.urls)),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]