from rest_framework import serializers

from polls.models import Poll, Question, Answer, UserAnswer, QuestionType


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'title', 'start_date', 'finish_date', 'description']

    def validate(self, data):
        if data['finish_date'] > data['start_date']:
            raise serializers.ValidationError("finish must occur after start")
        return data


class PollUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'title', 'finish_date', 'description']

    def validate(self, data):
        if data['finish_date'] > data['start_date']:
            raise serializers.ValidationError("finish must occur after start")
        return data


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'text', 'qtype']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text']


class QuestionDetailSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'poll', 'text', 'qtype', 'answers',]


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'selected_answers', 'typed_answer']

    def validate(self, data):
        q = data['question']
        if not q.poll.is_active():
            raise serializers.ValidationError("You cannot polling old poll")

        if not (bool(data['typed_answer']) ^ bool(data['selected_answers'])):
            if q.qtype == QuestionType.TEXT:
                raise serializers.ValidationError('Text type answer for this question')
            else:
                raise serializers.ValidationError('Choice answer from list for this question')
        if q.qtype == QuestionType.TEXT and not data['typed_answer']:
            raise serializers.ValidationError('Text type answer for this question')
        if q.qtype != QuestionType.TEXT and not data['selected_answers']:
            raise serializers.ValidationError('Choice answer from list for this question')

        return data


class PassedQuestionDetailSerializer(QuestionDetailSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    users_answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'poll', 'text', 'qtype', 'answers', 'users_answers']


class PassedPollSerializer(serializers.ModelSerializer):
    questions = PassedQuestionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = [
            'id', 'title', 'start_date', 'finish_date', 'description',
            'questions',
        ]

