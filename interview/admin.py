from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Question, Answer, Choice, Interview


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse(f'admin:{instance._meta.app_label}_{instance._meta.model_name}_change', args=[instance.pk])
        if instance.pk:
            return mark_safe(f'<a href="{url}" target="_blank">Редактировать вопрос в отдельном окне</a>')
        return ''
    edit_link.short_description = 'Ссылка на редактирование'


class QuestionInline(EditLinkToInlineObject, admin.TabularInline):
    model = Question
    extra = 2
    readonly_fields = ('edit_link', )


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class OneChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_active',
    )
    inlines = [ChoiceInline, OneChoiceInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if obj and obj.extra_fields_by_choice() == inline.__class__.__name__:
                yield inline.get_formset(request, obj), inline


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'question',
        'lock_other',
    )
    list_filter = ('question',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'question',
        'choice',
    )
    list_filter = ('user_id',)
