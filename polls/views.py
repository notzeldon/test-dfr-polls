from django.http import Http404
from django.utils.timezone import localtime
from rest_framework import generics
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers


# Base


class BasePollAPIView(generics.GenericAPIView):
    queryset = models.Poll.objects.all()
    serializer_class = serializers.PollSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id',]
    permission_classes = [permissions.IsAuthenticated]


class BaseQuestionAPIView(generics.GenericAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'poll']
    permission_classes = [permissions.IsAuthenticated]


class BaseAnswerAPIView(generics.GenericAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'question']
    permission_classes = [permissions.IsAuthenticated]

# For administrate


class AdminPollView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView, BasePollAPIView):

    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method in ['GET', 'POST']:
            return serializers.PollSerializer
        else:
            return serializers.PollUpdateSerializer

    def get_object(self):
        if self.request.method not in ['GET', 'POST']:
            return self.queryset.get(id=self.request.query_params.get('id'))
        return super().get_object()


class AdminQuestionView(
    generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView,
    BaseQuestionAPIView
):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        if self.request.method not in ['GET', 'POST']:
            return self.queryset.get(id=self.request.query_params.get('id'))
        return super().get_object()


# For users

class PollView(generics.ListAPIView, BasePollAPIView):
    """Returns active polls
    """

    def get_queryset(self):
        now = localtime()
        return models.Poll.objects.filter(start_date__lte=now, finish_date__gt=now)


class QuestionView(generics.ListAPIView, BaseQuestionAPIView):

    def get_serializer_class(self):
        if self.request.query_params.get('id'):
            return serializers.QuestionDetailSerializer
        else:
            return super().get_serializer_class()

    def get_queryset(self):
        now = localtime()
        return super().get_queryset().filter(poll__start_date__lte=now, poll__finish_date__gt=now)

    def get_object(self):
        obj = super().get_object()
        poll_id = self.request.GET.get('poll') or ''
        if poll_id.isdigit():
            poll_id = int(poll_id)
        if not obj.poll.is_active() or obj.poll_id != poll_id:
            raise Http404
        return obj


class AnswerView(generics.ListCreateAPIView, BaseAnswerAPIView):
    pass


# Polling

class QuestionPollingView(generics.CreateAPIView):
    """Returns list non-passed questions for poll

    # TODO: Fix multiple answers
    """
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.UserAnswerSerializer
    queryset = models.UserAnswer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PassedPollsView(generics.ListAPIView, BasePollAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = serializers.PassedPollSerializer

    def get_queryset(self):
        return super().get_queryset().filter(questions__users_answers__user=self.request.user)






