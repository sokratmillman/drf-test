import nested_admin
from django.contrib import admin

from .models import Choice, Question, Result, Test


class ChoiceInline(nested_admin.NestedTabularInline):
    model = Choice
    classes = ['collapse']
    extra = 0

    def get_min_num(self, request, obj=None, **kwargs):
        if obj and obj.question_type and obj.question_text:
            return 2


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [ChoiceInline,]
    classes = ['collapse']
    extra = 0

    def get_min_num(self, request, obj=None, **kwargs):
        if obj and obj.num_of_questions:
            self.classes = []
            return obj.num_of_questions

    def get_max_num(self, request, obj=None, **kwargs):
        if obj and obj.num_of_questions:
            return obj.num_of_questions


class TestAdmin(nested_admin.NestedModelAdmin):
    list_per_page = 5
    list_filter = (
        'is_published',
    )
    search_fields = (
        'test_name',
    )

    def get_inlines(self, request, obj=None):
        if obj and obj.num_of_questions:
            return [QuestionInline,]
        return []


class ResultAdmin(admin.ModelAdmin):
    list_per_page = 5
    search_fields = (
        'test_name',
        'username',
    )
    readonly_fields = [field.name for field in Result._meta.get_fields()]


admin.site.register(Test, TestAdmin)
admin.site.register(Result, ResultAdmin)
