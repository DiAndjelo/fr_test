import uuid

from django.conf import settings
from django.db import models


QUESTION_CHOICES = [
    ('text', 'Ответ текстом'),
    ('one_choice', 'Ответ с выбором одного варианта'),
    ('some_choices', 'Ответ с выбором нескольких вариантов')
]


class Interview(models.Model):
    """
    Модель опроса
    """
    name = models.CharField(max_length=512, null=True, verbose_name='Название опроса')
    date_start = models.DateTimeField(verbose_name='Дата создания опроса')
    date_end = models.DateTimeField(verbose_name='Дата окончания опроса')
    description = models.TextField(null=True, verbose_name='Описание опроса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    """
    Модель вопроса в опросе
    """
    interview = models.ForeignKey(Interview, on_delete=models.DO_NOTHING)
    title = models.TextField(null=True, verbose_name='Текст вопроса')
    is_active = models.BooleanField(default=False, verbose_name='Видимость для пользователя')
    type = models.CharField(max_length=128, choices=QUESTION_CHOICES, verbose_name='Тип вопроса')

    def __str__(self):
        return self.title

    def extra_fields_by_choice(self):
        if self.type == 'text':
            extra_inline_model = 'OneChoiceInline'
            return extra_inline_model
        if self.type == 'one_choice' or self.type == 'some_choices':
            extra_inline_model = 'ChoiceInline'
            return extra_inline_model

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    """
    Модель выбора ответа в вопросе
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=4096, verbose_name='Название выбора')
    lock_other = models.BooleanField(default=False, verbose_name='Заблокировать остальные?')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Выбор в вопросе'
        verbose_name_plural = 'Выборы в вопросе'


class Answer(models.Model):
    """
    Модель ответа на вопрос
    """
    user_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    choice = models.ForeignKey(Choice, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice.title

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопрос'
