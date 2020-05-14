from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


USER_MODEL = get_user_model()

'''
добавление/изменение/удаление опросов. 
Атрибуты опроса: название, дата старта, дата окончания, описание. 
После создания поле "дата старта" у опроса менять нельзя

добавление/изменение/удаление вопросов в опросе. 
Атрибуты вопросов: текст вопроса, тип вопроса 
(ответ текстом, ответ с выбором одного варианта, 
ответ с выбором нескольких вариантов)
'''


class Poll(models.Model):

    class Meta:
        verbose_name = _('poll')

        ordering = ['-start_date']

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
    )

    start_date = models.DateTimeField(
        verbose_name=_('start on'),
        db_index=True,
    )

    finish_date = models.DateTimeField(
        verbose_name=_('finish on'),
        db_index=True,
    )

    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )

    def __str__(self):
        return self.title


'''
Атрибуты вопросов: текст вопроса, тип вопроса 
(ответ текстом, ответ с выбором одного варианта, 
ответ с выбором нескольких вариантов)
'''


class QuestionType:
    """Question type. Support class for question field "qtype"
    """

    TEXT = 1
    ONE_OPTION = 2
    SEVERAL_OPTIONS = 3

    choices = {
        TEXT: _('text'),
        ONE_OPTION: _('one option'),
        SEVERAL_OPTIONS: _('several options'),
    }


class Question(models.Model):
    """Question for poll
    """

    class Meta:
        verbose_name = _('question')

        ordering = ['text']

    poll = models.ForeignKey(
        to=Poll,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    text = models.CharField(
        verbose_name=_('text'),
        max_length=255,
    )

    qtype = models.IntegerField(
        verbose_name=_('type'),
        choices=QuestionType.choices.items(),
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Answer for question
    """

    class Meta:
        verbose_name = _('answer')

        ordering = ['text']

    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    # TODO: `text` field can be modified to TextField in future
    text = models.CharField(
        verbose_name=_('text'),
        max_length=255,
    )

    def __str__(self):
        return self.text


class UserAnswer(models.Model):

    class Meta:
        verbose_name = _("user's answer")

        ordering = ['id']

    user = models.ForeignKey(
        verbose_name=_('user'),
        to=USER_MODEL,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    question = models.ForeignKey(
        to=Question,
        on_delete=models.CASCADE,
        related_name='users_answers',
    )

    selected_answers = models.ManyToManyField(
        verbose_name=_('selected answer'),
        to=Answer,
        related_name='+',
        blank=True,
    )

    typed_answer = models.CharField(
        verbose_name=_('typed answer'),
        max_length=255,
        null=True,
    )
