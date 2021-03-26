from django.urls import path, include
from rest_framework import routers

from interview.views import QuestionViewSet, AnswerViewSet, InterviewViewSet, ChoiceViewSet

router = routers.DefaultRouter()
router.register('questions', QuestionViewSet)
router.register('answers', AnswerViewSet)
router.register('interviews', InterviewViewSet)
router.register('choices', ChoiceViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
