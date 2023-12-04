from rest_framework import serializers

from .models import Choice, Question, Result, Test


class DashboardTestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    test_name = serializers.CharField()
    is_available = serializers.BooleanField()


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'choices']


class TestSerializer(serializers.ModelSerializer):
    depth = 2
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['test_name', 'questions']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        exclude = []
