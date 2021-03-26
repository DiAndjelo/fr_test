from rest_framework import serializers
from .models import Answer, Question, Choice, Interview


class ChoiceSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ['id', 'title', 'percent', 'lock_other', ]

    @staticmethod
    def get_percent(obj):
        total = Answer.objects.filter(question=obj.question).count()
        current = Answer.objects.filter(question=obj.question, choice=obj).count()
        if total != 0:
            return float(current * 100 / total)
        else:
            return float(0)


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source='choice_set', )

    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'choices', ]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class InterviewSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Interview
        fields = '__all__'
